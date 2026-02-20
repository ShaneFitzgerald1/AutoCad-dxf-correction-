import math 
from backend.mathematical import Mathematical

maths = Mathematical

class datafiltration: 
    @staticmethod
    def remove_duplicate_lines(all_lines, line_refs):
        #Function removes any duplicate lines ensuring there are no line repeats
        seen = []
        duplicate_refs = []
        
        for idx, line in enumerate(all_lines):
            if line in seen:
                duplicate_refs.append(line_refs[idx])
            seen.append(line)

        return duplicate_refs
    
    @staticmethod
    def On_Channel_Line(Blockref_Points, all_walls, insert_refs, line_properties, tolerance=1, tolerance_2=5 ): 
    #This function checks all block references to see if they are on a line. If Yes a Correct result is appended
    #If blcoks are within lines to a certain degree their position is fixed to the line using minimum perpendicular distance to a line
    #If there the block reference is near no lines an error is return 
    #Function inputs: Filepath, Tolerence1 (if something is within this its not a mistake), Tolerence2 if it falls within this and outside T1 its a mistake 

        filtered_blockref, filtered_walls, filtered_insert_refs = maths.Shape_outline(Blockref_Points, all_walls, insert_refs)

        blocks_on_line= []
        mistake_points = []
        correct_blocks = []
        corrected_blocks = []
        correct_block_refs = []
        corrected_block_refs = []
    
        # Use enumerate to get both index and block data
        for idx, block in enumerate(filtered_blockref):
            name = block[0]
            x = block[1]
            y = block[2]
            angle = block[3]
            name_error = block[4]
        
            # Find the closest corner to this block
            closest_corner = None
            min_corner_dist = float('inf') #set the value intially to an infinitily large distance 
            
            for wall in filtered_walls: #defining the x and y wall points on channel outline 
                x_wall = wall[0]
                y_wall = wall[1]
                distance_corner = math.sqrt((x_wall - x)**2 + (y_wall - y)**2)
                
                if distance_corner < min_corner_dist:
                    min_corner_dist = distance_corner #set the corner distance found to the minimum corner distance 
                    closest_corner = (x_wall, y_wall)

            found_match = False
            
            #Situation 1: Check for exact matches (within tolerance)
            for i in range(len(line_properties)):
                slope, intercept, xs, ys, xe, ye = line_properties[i]
        
                # Case 1: Vertical line
                if slope is None:
                    x_intercept = float(intercept.split()[2]) #Pulling the float value out 
                    distance = abs(x - x_intercept)
                    
                    if distance <= tolerance: #if the distance is less than the tolerance we've found a match, this logic applies to all cases 
                        blocks_on_line.append([name, x, y, angle, i, 'vertical', 'On Line', 'Exact'])  #store for interface table presentation 
                        correct_blocks.append([name, x, y, angle, name_error])   #Store for creating new dxf 
                        correct_block_refs.append(filtered_insert_refs[idx])  # ← Use filtered refs with idx
                        found_match = True
                        break
                
                # Case 2: Normal line with slope
                else:
                    expected_y = slope * x + intercept
                    distance = abs(y - expected_y)
                    
                    if distance <= tolerance:
                        blocks_on_line.append([name, x, y, angle, i, 'normal', 'On Line', 'Exact'])
                        correct_blocks.append([name, x, y, angle, name_error])
                        correct_block_refs.append(filtered_insert_refs[idx])  # ← Use filtered refs with idx
                        found_match = True
                        break
            
            #Situation 2: Look for near matches 
            if not found_match:
                for i in range(len(line_properties)):
                    slope, intercept, xs, ys, xe, ye = line_properties[i]
                    
                    #Blocks are being checked against the equation of lines of other lines, an equation of a line assumes a lines length is infinite throuhgh space
                    #the below code stops checking lines that are far from the block being checked to be corrected onto that line 
                    avoid_distant_lines = (xs <= x <= xe or xe <= x <= xs or ys <= y <= ye or ye <= y <= y)
                                
                    min_distance = min(abs(x - xs), abs(x - xe),   #find miniumum distance to the line if not within the range    
                        abs(y - ys), abs(y - ye))
                    
                    if not avoid_distant_lines and (min_distance > 5):  #if the block is not within the range of the line then check if it is within a tolerence, than skip that line
                        continue 

                    # Case 1: Vertical line
                    if slope is None:
                        x_intercept = float(intercept.split()[2])
                        distance = abs(x - x_intercept)
                        
                        if distance <= tolerance_2:
                            blocks_on_line.append([name, x, y, angle, i, 'vertical', 'Near Line', 'Warning'])
                            
                            if min_corner_dist <= 5: #If its within 5 of a corner move the block reference to the nearest corner 
                                mistake_points.append([name, x, y, closest_corner[0], closest_corner[1]])   #Store for interface presnetaion 
                                corrected_blocks.append([name, closest_corner[0], closest_corner[1], angle, name_error]) #Store for dxf 
                                corrected_block_refs.append(filtered_insert_refs[idx])  # ← Use filtered refs with idx

                            else:
                                mistake_points.append([name, x, y, x_intercept, y])  #Store for Interface Presentation
                                corrected_blocks.append([name, x_intercept, y, angle, name_error])   # Store for dxf 
                                corrected_block_refs.append(filtered_insert_refs[idx])  # ← Use filtered refs with idx
                            
                            found_match = True
                            break
                    
                    # Case 2: Normal line with slope, Holds same logic as above code 
                    else:
                        expected_y = slope * x + intercept
                        distance = abs(y - expected_y)
                        
                        if distance <= tolerance_2:
                            blocks_on_line.append([name, x, y, angle, i, 'normal', 'Near Line', 'Warning'])
                            
                            if min_corner_dist <= 5:
                                mistake_points.append([name, x, y, closest_corner[0], closest_corner[1]])
                                corrected_blocks.append([name, closest_corner[0], closest_corner[1], angle, name_error])
                                corrected_block_refs.append(filtered_insert_refs[idx])  # ← Use filtered refs with idx

                            else: #We have a Point and  a slope, the below finds the minimum perpendicular distance from the orignal point to that line
                                #The code returns the x and y points on that line where the intersection occurs, thus becoming the fixed point. 
                                x_fixed = (x + slope * (y - intercept)) / (slope**2 + 1) 
                                y_fixed = (slope*x + y*slope**2 + intercept) / (slope**2 + 1)
                                mistake_points.append([name, x, y, x_fixed, y_fixed])
                                corrected_blocks.append([name, x_fixed, y_fixed, angle, name_error])
                                corrected_block_refs.append(filtered_insert_refs[idx])  # ← Use filtered refs with idx
                        
                            found_match = True
                            break
            
            if not found_match: #No matches found at all within either tolerence return an error
                blocks_on_line.append([name, x, y, angle, None, None, 'Not On Line', 'Error']) 

        final_corrected_blocks, final_corrected_refs = datafiltration.filter_name_errors(correct_blocks, correct_block_refs, corrected_blocks, corrected_block_refs)         
        
        return blocks_on_line, mistake_points, final_corrected_blocks, final_corrected_refs, filtered_walls
    
    @staticmethod
    def filter_name_errors(correct_blocks, correct_block_refs, corrected_blocks, corrected_block_refs):
        #Function that filters through all blocks to see if there is a name error and returns it as a mistake 
        final_correct_blocks = []
        final_correct_refs = []
        final_corrected_blocks = list(corrected_blocks)
        final_corrected_refs = list(corrected_block_refs)

        for idx, block in enumerate(correct_blocks):
            name, x, y, angle, name_error = block
            if name_error:
                final_corrected_blocks.append(block)
                final_corrected_refs.append(correct_block_refs[idx])
            else:
                final_correct_blocks.append(block)
                final_correct_refs.append(correct_block_refs[idx])

        return final_corrected_blocks, final_corrected_refs
    
    @staticmethod 
    def find_line_error(all_lines, all_walls, line_refs, line_properties, wall_slopes, wall_intercepts, tolerance=1): 
    #This function goes through all the lines searching for errors. All lines should start and end at another line 
    #Unless it is on the channel outline in which case the check just ensures hte line is on the channel outline  
    #The code ensures that the end points of each line are on another line, there is a clause to prevent a line from checking itself against its own line
    #If a mistake is identified in a line the closest slope and y intercept are returned (i.e the equation of the line that is closest to that line is returned)
    # If a mistake is identified being too large the point will be returend as a mistake but no intercept or slope will be provided
    #  Thus mistake is flagged, no reasonable fix assumption for code to make

        line_mistakes = []
        correct_lines = []
        line_mistake_refs = []
        correct_line_refs = []

        for idx, line in enumerate(all_lines):  #Each start and end ponit of the line are checked against the slope and intercepts of the checker lines 
            name = line[0]                
            x_start = line[1]
            y_start = line[2]
            x_end = line[3]
            y_end = line[4]

            start_matches = False 
            end_matches = False 
            
            # Track closest lines for start and end points
            closest_start_slope = None
            closest_start_intercept = None
            min_start_dist = float('inf')
            temp_start_slope = None
            temp_start_intercept = None
            
            closest_end_slope = None
            closest_end_intercept = None
            min_end_dist = float('inf')
            temp_end_slope = None
            temp_end_intercept = None

            min_x = min(x for wall in all_walls for x, y in wall) #finding the boundaries of the shape 
            min_y = min(y for wall in all_walls for x,y in wall)
            max_x = max(x for wall in all_walls for x, y in wall)
            max_y = max(y for wall in all_walls for x, y in wall)

            # Check boundaries ONCE (no loop needed)
            if x_start < min_x or x_start > max_x or y_start < min_y or y_start > max_y: 
                start_matches = False 
            if x_end < min_x or x_end > max_x or y_end < min_y or y_end > max_y: 
                end_matches = False 

            wall_line_match = False
            for i in range(len(wall_slopes)): 
                wall_slope = wall_slopes[i]
                wall_intercept = wall_intercepts[i]
                
                # Main check for a point on the channel outline
                if wall_slope is None:  # Vertical wall
                    x_intercept = float(wall_intercept.split()[2]) 
                    x_sd = abs(x_intercept - x_start)
                    x_ed = abs(x_intercept - x_end)
                    if x_ed < 0.1 and x_sd < 0.1:
                        start_matches = True 
                        end_matches = True
                        wall_line_match = True
                        break  
                else:  # Wall with slope
                    y_ss = abs(y_start - (wall_slope * x_start + wall_intercept))
                    y_ee = abs(y_end - (wall_slope * x_end + wall_intercept))
                    if y_ss < 0.1 and y_ee < 0.1: 
                        start_matches = True 
                        end_matches = True
                        wall_line_match = True
                        break

            if wall_line_match: # if the wall is completly on the channel outline skip checking against the other lines 
                correct_lines.append([name, x_start, y_start, x_end, y_end])
                correct_line_refs.append(line_refs[idx])
                continue  # Skip to next line

            for prop_line in line_properties: #These are the checker lines all lines (not on the channel outline) are checked 
                slope, intercept, x_s, y_s, x_e, y_e = prop_line
                
                same_line_forward = (abs(x_s - x_start) < 0.01 and abs(y_s - y_start) < 0.01 and #avoid checking a line against itself 
                                    abs(x_e - x_end) < 0.01 and abs(y_e - y_end) < 0.01)
                same_line_reverse = (abs(x_s - x_end) < 0.01 and abs(y_s - y_end) < 0.01 and 
                                    abs(x_e - x_start) < 0.01 and abs(y_e - y_start) < 0.01)
                
                avoid_same_formula_error = (abs(x_start - x_s) < 0.1 and abs(x_end - x_e) < 0.1  #if two vertical lines are on the same path 
                                            and abs(y_start - y_s) > 10 and abs(y_end - y_e) > 10) #skip this line if its two far away 
                avoid_reverse_formula_error = (abs(x_start - x_e) < 0.1 and abs(x_end - x_s) < 0.1 
                                            and abs(y_start - y_e) > 10 and abs(y_end - y_s) > 10)
                
                #Lines are being checked against the equation of lines of other lines, an equation of a line assumes a lines length is infinite throuhgh space
                #the below code stops checking lines that are far from the line being checked to be corrected onto that line 
                avoid_distance_lines = (x_s <= x_start <= x_e or x_e <= x_start <= x_s or x_s <= x_end <= x_e  #if hte line is out of range of hte checking line
                                    or x_e <= x_end <= x_s  or y_s <= y_start <= y_e or y_e <= y_start <= y_s
                                    or y_s <= y_end <= y_e or y_e <= y_end <= y_s)
                
                min_distance = min(abs(x_start - x_s), abs(x_start - x_e),   #find miniumum distance to the line if not within the range
                    abs(x_end - x_s), abs(x_end - x_e),    
                    abs(y_start - y_s), abs(y_start - y_e), 
                    abs(y_end - y_s), abs(y_end - y_e))
                
                if same_line_forward or same_line_reverse or avoid_reverse_formula_error or avoid_same_formula_error:
                    continue 
                if not avoid_distance_lines and (min_distance > 5):  #if the line is not within the range of the line then check if it is within a tolerence, than skip that line
                    continue 

                # Check start point and track closest - ONLY STORE TEMP VALUES
                if not start_matches:
                    start_dist = maths.find_distance_to_line(x_start, y_start, slope, intercept)
                    if start_dist <= tolerance: 
                            start_matches = True
                        
                    if start_dist < min_start_dist:
                        min_start_dist = start_dist
                        temp_start_slope = slope
                        temp_start_intercept = intercept

                # Check end point and track closest
                if not end_matches:      
                    end_dist = maths.find_distance_to_line(x_end, y_end, slope, intercept) 
                    if end_dist <= tolerance: 
                            end_matches = True
                    if end_dist < min_end_dist:
                            min_end_dist = end_dist
                            temp_end_slope = slope
                            temp_end_intercept = intercept        

                if start_matches and end_matches: #If a match is found break 
                    break         

            #The below code takes the temp slopes and intercepts found in the above code, slopes and intercepts are split into different 
            if min_start_dist <= 25:
                closest_start_slope = temp_start_slope
                closest_start_intercept = temp_start_intercept
            elif 25 < min_start_dist < 35:
                closest_start_slope = None
                closest_start_intercept = None
            elif min_start_dist > 35: 
                start_matches = True    

            if min_end_dist <= 25: 
                closest_end_slope = temp_end_slope
                closest_end_intercept = temp_end_intercept
            elif 25 < min_end_dist < 35:
                closest_end_slope = None
                closest_end_intercept = None
            elif min_end_dist > 35: 
                end_matches = True 
            
            if not start_matches or not end_matches:  
                line_mistakes.append([name, x_start, y_start, x_end, y_end, closest_start_slope, closest_start_intercept, closest_end_slope, closest_end_intercept])
                line_mistake_refs.append(line_refs[idx])
            else: 
                correct_lines.append([name, x_start, y_start, x_end, y_end])   
                correct_line_refs.append(line_refs[idx])          

        return line_mistakes, correct_lines, line_mistake_refs, correct_line_refs
    
    @staticmethod
    def fix_line_mistakes(line_mistakes, line_mistake_refs): 
    #This function fixes any errors recored in the find_line_error function, mathamtically vertical lines are account for in all scenarios 
    #If both lines have slopes, functions are solved using simealtaneous equations 
    #The function returns a list of fixed lines with their name, position, layer, and colour. 
        fixed_lines = []
        fixed_lines_box = []
        
        for line in line_mistakes: 
            name = line[0]
            x_start = line[1]
            y_start = line[2]
            x_end = line[3]
            y_end = line[4]
            closest_start_slope = line[5]
            closest_start_intercept = line[6]
            closest_end_slope = line[7]
            closest_end_intercept = line[8]
        
            #Basically if line is too far away form anything leave it as it is (it is supposed to be like that)
            if (closest_start_slope is None and closest_start_intercept is None) or (closest_end_slope is None and closest_end_intercept is None): 
                new_x_start = x_start 
                new_y_start = y_start 
                new_x_end = x_end
                new_y_end = y_end

                fixed_lines.append([name, new_x_start, new_y_start, new_x_end, new_y_end]) #Append these results so they are no longer checked
                fixed_lines_box.append([name, new_x_start, new_y_start, new_x_end, new_y_end, closest_start_slope, closest_start_intercept, closest_end_slope, closest_end_intercept])
                continue

            elif x_start == x_end:  # Vertical line

                if closest_start_slope is None: #This is unlikely scenario, if both lines are vertical, probably that line is offset so it gets snapped onto the vertical line closest to it. 
                    x_intercept_start = float(closest_start_intercept.split()[2])
                    new_x_start = x_intercept_start 
                    new_y_start = y_start 
                else:
                    new_x_start = x_start  #if line has a slope 
                    new_y_start = closest_start_slope * x_start + closest_start_intercept #calculate where new y should be based on original line 
                
                if closest_end_slope is None: #same as above but for the end 
                    x_intercept_end = float(closest_end_intercept.split()[2])
                    new_x_end = x_intercept_end
                    new_y_end = y_end
                else:
                    new_x_end = x_end
                    new_y_end = closest_end_slope * x_end + closest_end_intercept
            
            else: #if slope of original line is not None 
                slope_line = (y_end - y_start) / (x_end - x_start) #original line has a slope value 
                intercept_line = y_start - slope_line * x_start  

                # FIX START POINT
                if closest_start_slope is None:
                    x_intercept_start = float(closest_start_intercept.split()[2])
                    new_x_start = x_intercept_start #new start point for the line will be x point on closest line 
                    new_y_start = slope_line * new_x_start + intercept_line  #plug new start x into formula to find new y point 
                        
                else: #both lines have slopes call sim eq func 
                    new_x_start, new_y_start = maths.solve_simultaneous_equations(closest_start_slope, closest_start_intercept, slope_line, intercept_line)

                # Fix the end points, same logic as above. 
                if closest_end_slope is None:
                    x_intercept_end = float(closest_end_intercept.split()[2]) #move the line to the x point
                    new_x_end = x_intercept_end #move the line to the x point
                    new_y_end = slope_line * new_x_end + intercept_line #sub into equation to find new y point 
                        
                else: #Both lines have slopes call sim eq func 
                    new_x_end, new_y_end = maths.solve_simultaneous_equations(closest_end_slope, closest_end_intercept, slope_line, intercept_line)

            fixed_lines.append([name, new_x_start, new_y_start, new_x_end, new_y_end])
            fixed_lines_box.append([name, new_x_start, new_y_start, new_x_end, new_y_end, closest_start_slope, closest_start_intercept, closest_end_slope, closest_end_intercept])
            
        return fixed_lines, fixed_lines_box, line_mistake_refs
    

    @staticmethod
    def find_fixed_line_points(line_mistakes, fix_line_box): 
    #Lines are stored with their start and end values so we need another function determine precisley what point the mistake was at so it can be highlighted in dxf 
    #this function checks for differnce between line mistakes and fixed lines to see what points change, the points that change are appended

        line_mistake_points = []
        find_error = []
        none_error = []
        
        for i in range(len(line_mistakes)): 
            line_mistake = line_mistakes[i]
            fixed_line = fix_line_box[i]
    
            x_start_m = line_mistake[1]
            y_start_m = line_mistake[2]
            x_end_m = line_mistake[3]
            y_end_m = line_mistake[4]

            x_start_f = fixed_line[1]
            y_start_f = fixed_line[2]
            x_end_f = fixed_line[3]
            y_end_f = fixed_line[4]
            cl_st_slope = fixed_line[5]
            cl_st_intercept = fixed_line[6]
            cl_ed_slope = fixed_line[7]
            cl_ed_intercept = fixed_line[8]

            if abs(x_start_m - x_start_f) >= 0.1 or abs(y_start_m - y_start_f) >= 0.1: 
                line_mistake_points.append([x_start_f, y_start_f])
                find_error.append([x_start_f, y_start_f])

            if abs(x_end_m - x_end_f) >= 0.1 or abs(y_end_m - y_end_f) >= 0.1: 
                line_mistake_points.append([x_end_f, y_end_f]) 
                find_error.append([x_end_f, y_end_f])
            
            if cl_st_slope is None and cl_st_intercept is None: 
                line_mistake_points.append([x_start_f, y_start_f]) 
                none_error.append({x_start_f, y_start_f}) 
                    
            if cl_ed_slope is None and cl_ed_intercept is None: 
                line_mistake_points.append([x_end_f, y_end_f])
                none_error.append([x_end_f, y_end_f])

        return line_mistake_points  


                

