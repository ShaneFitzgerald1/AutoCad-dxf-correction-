import ezdxf
from ezdxf.lldxf import const
import subprocess
import os
import numpy as np
import pandas as pd
import math
from sympy import symbols, Matrix, Eq, solve
from dataclasses import dataclass
from backend.mathematical import Mathematical
from backend.guipresentation import presentation
from backend.datafiltration import datafiltration

maths = Mathematical()
pres = presentation() 
filter = datafiltration()

def autocad_points(filepath): 
    #This function extracts all necessasry data for analysis from the autocad file. 
    # Inputs are filepath (the autocad file itself)
    #Outputs are: Block references points, DiagonalBrace_Points (start and end position of all lines), All Walls (Wall points, points on the channel outline)
    doc = ezdxf.readfile(filepath)
    msp = doc.modelspace()
    
    Blockref_Points = []
    all_lines = []
    all_walls = []  
    insert_refs = []
    line_refs = []
    block_names = []
    new_names = []
   
    for insert in msp.query('INSERT'): 
        insert_refs.append(insert)

        blockName = insert.dxf.name
        block_names.append([blockName])
        if blockName.startswith('*U'): #Dynamic block
            block = doc.blocks.get(blockName)
            blockRecord = block.block_record
            try:
                if xdata := blockRecord.get_xdata("AcDbBlockRepBTag"):
                    for tag in xdata:
                        if tag.code == 1005: #xdata tag to store reference handle
                            ogHandle = tag.value
                            for b in doc.blocks: #Look through all blocks to find original reference block (handle match)
                                if b.dxf.handle == ogHandle:
                                    name = b.dxf.name #Use the name of the original block
                                    block_def = b  # *** NEW: Store block definition for offset calculation ***
            except const.DXFValueError: #Doesn't have indirect dynamic block tag or xdata not available
                print("Not a dynamic block")
                name = blockName
                block_def = block  # *** NEW: Use current block if not dynamic ***

        else: #Non-dynamic standard block
            name = blockName
            block_names.append([blockName])
            block_def = doc.blocks.get(blockName)  # *** NEW: Get block definition for standard blocks ***

        # Original insertion point from the block reference
        x = round(insert.dxf.insert.x, 2)
        y = round(insert.dxf.insert.y, 2) 
        angle = round(insert.dxf.rotation, 2)
     
        offset_found = False 
        name_error = False 

        for entity in block_def:
            if entity.dxftype() == 'INSERT':
                x_offset = entity.dxf.insert.x   #find offset inside block 
                y_offset = entity.dxf.insert.y
                new_name = entity.dxf.name        #find 
                new_names.append([new_name])
                if x_offset > 0.01 and y_offset > 0.01:
                    x_final = x + x_offset 
                    y_final = y + y_offset 
                    offset_found = True 
                if new_name != name: 
                    name_error = True 
                if new_name == name: 
                    name_error = False     
         
        attrib_data = {}  #reset each iteration
        if insert.has_attrib:
            for attrib in insert.attribs:
                attrib_data[attrib.dxf.tag] = attrib.dxf.text 
             
        if offset_found: 
            Blockref_Points.append([new_name, x_final, y_final, angle, name_error])
        else: 
            Blockref_Points.append([name, x, y, angle, name_error])

    # Extract LINE data
    for line in msp.query('LINE'):
        line_refs.append(line)
        layer = line.dxf.layer
        name = blockName 
        start_x = round(line.dxf.start.x, 2)
        start_y = round(line.dxf.start.y, 2)
        end_x = round(line.dxf.end.x, 2)
        end_y = round(line.dxf.end.y, 2)
    
        all_lines.append([layer, start_x, start_y, end_x, end_y])      
    
    # Extract POLYLINE data 
    for polyline in msp.query('LWPOLYLINE[layer=="CHANNEL OUTLINE"]'):
        points = extract_polyline_points(polyline)
        all_walls.append(points)

    wall_lengths = maths.wall_len(all_lines)  
    slopes, y_intercepts, line_properties, wall_slopes, wall_intercepts = maths.slope_values(all_lines, all_walls) 
    wall_slope_intercept = pres.combine_slope_walls(wall_lengths, slopes, y_intercepts)
    (blocks_on_line, mistake_points, final_corrected_blocks,
     final_corrected_refs, filtered_walls) = filter.On_Channel_Line(Blockref_Points, all_walls, insert_refs, line_properties, tolerance=1, tolerance_2=5)
    
    # final_corrected_blocks, final_corrected_refs = filter.filter_name_errors(correct_blocks, correct_block_refs, corrected_blocks, corrected_block_refs)    

    on_line_points, all_lines_table = pres.what_line(blocks_on_line, filtered_walls, all_lines, tolerance = 1)
    (line_mistakes, correct_lines, 
     line_mistake_refs, correct_line_refs) = filter.find_line_error(all_lines, all_walls, line_refs, line_properties, wall_slopes, wall_intercepts, tolerance=1)
    fixed_lines, fixed_lines_box, line_mistake_refs = filter.fix_line_mistakes(line_mistakes, line_mistake_refs)
    line_mistake_points = filter.find_fixed_line_points(line_mistakes, fixed_lines_box)
    duplicate_line_refs, line_duplicate_points = filter.remove_duplicate_lines(all_lines, line_refs)

    # scaled_blocks, mirrored_blocks = check_block_scaling(filepath)
    return (doc, on_line_points, all_lines_table, 
        wall_slope_intercept, filtered_walls, mistake_points, 
        final_corrected_blocks, line_mistakes, fixed_lines, final_corrected_refs, 
        line_mistake_points, line_mistake_refs, duplicate_line_refs, line_duplicate_points)

def extract_polyline_points(polyline): #Convert wall points into x and y points 
        if polyline.dxftype() == 'LWPOLYLINE':
            wall_points = []
            for point in polyline.get_points():
                x = float(round(point[0], 1))  
                y = float(round(point[1], 1))  
                wall_points.append([x, y])
            return wall_points
        return []

def update_dxf_in_place(filepath, output_filepath):
    #This function updates the dxf file, function updates Block reference and line positions based on corrections
    # Red box is drawn around Block reference mistakes and a Red circle is drawn around line mistakes. 

    (doc, on_line_points, all_lines_table, 
        wall_slope_intercept, filtered_walls, mistake_points, 
        corrected_blocks, line_mistakes, fixed_lines, corrected_block_refs, 
        line_mistake_points, line_mistake_refs, duplicate_line_refs, duplicate_line_points) = autocad_points(filepath)
    
    msp = doc.modelspace()

    if 'CORRECTION_HIGHLIGHT' not in doc.layers:
        correction_layer = doc.layers.new('CORRECTION_HIGHLIGHT')
        correction_layer.color = 1

    for idx, block_data in enumerate(corrected_blocks):
        name = block_data[0]
        new_x, new_y = block_data[1], block_data[2]
        entity = corrected_block_refs[idx]
        entity.dxf.insert = (new_x, new_y)
        entity.dxf.name = name 
        draw_red_box(msp, new_x, new_y, 80)

    for idx, line_data in enumerate(fixed_lines):
        name = line_data[0]
        new_x_start, new_y_start = line_data[1], line_data[2]
        new_x_end, new_y_end = line_data[3], line_data[4]
        entity = line_mistake_refs[idx]
        entity.dxf.start = (new_x_start, new_y_start)
        entity.dxf.end = (new_x_end, new_y_end)

    for point in line_mistake_points:
        x, y = point[0], point[1]
        msp.add_circle(center=(x, y), radius=50, dxfattribs={"color": 1})

    for entity in duplicate_line_refs:
        msp.delete_entity(entity)    

    for line in duplicate_line_points: 
        x_s, y_s, x_e, y_e = line 
        draw_triangle(msp, x_s, y_s)
        draw_triangle(msp, x_e, y_e)

    doc.saveas(output_filepath)

def draw_red_box(msp, x, y, size):
    """Draws a red rectangle around corrected block references"""
    corners = [
        (x - size, y - size),
        (x + size, y - size),
        (x + size, y + size),
        (x - size, y + size),
    ]
    msp.add_lwpolyline(corners, close=True, dxfattribs={'layer': 'CORRECTION_HIGHLIGHT', 'color': 1})

def draw_triangle(msp, x, y): 
    displacement = 60
    point1 = x, y + displacement
    point2 = x + displacement * math.cos(-0.523599), y + displacement * math.sin(-0.523599)
    point3 = x + displacement * math.cos(3.66519), y + displacement * math.sin(3.66519)   
    points = [point1, point2, point3]
    msp.add_lwpolyline(points, close=True, dxfattribs={'layer': 'CORRECTION_HIGHLIGHT', 'color': 1})

