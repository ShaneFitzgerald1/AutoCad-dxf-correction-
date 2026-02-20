from sympy import symbols, Eq, solve
import math

class Mathematical:
    
    @staticmethod
    def wall_len(all_lines):
        wall_lengths = []
        for line in all_lines:
            name, x_start, y_start, x_end, y_end = line
            delta_x = x_start - x_end
            delta_y = y_start - y_end
            distance = math.sqrt((delta_x)**2 + (delta_y)**2)
            wall_lengths.append(distance)
        return wall_lengths
    
    @staticmethod
    def slope_values(all_lines, all_walls):  #takes all lines and all_walls from autocad 
    #This function creates the equation of the line for each line (Channel outline and interior lines)
    #Functions accounts for vertical lines

        slopes = [] 
        y_intercepts = []
        line_properties = []
        wall_slopes = []
        wall_intercepts = []

        for line in all_lines: 
            name, x_start, y_start, x_end, y_end = line  
            line_slopes, line_intercepts = Mathematical.calc_slope(x_start, y_start, x_end, y_end)
            slopes.append(line_slopes)
            y_intercepts.append(line_intercepts)
            line_properties.append([line_slopes, line_intercepts, x_start, y_start, x_end, y_end])
                    
        for walls in all_walls:  
            for i in range(len(walls)):  
                p1 = walls[i]
                p2 = walls[(i+1) % len(walls)]

                slope_wall, intercept_wall = Mathematical.calc_slope(p1[0], p1[1], p2[0], p2[1])
                wall_slopes.append(slope_wall)
                wall_intercepts.append(intercept_wall)  
                line_properties.append([slope_wall, intercept_wall, p1[0], p1[1], p2[0], p2[1]])      

        return slopes, y_intercepts, line_properties, wall_slopes, wall_intercepts

    @staticmethod
    def calc_slope(x1, y1, x2, y2):
        if x1 == x2:
            slope = None
            c = f'X Intercept {x1}'
        else:
            slope = (y2 - y1) / (x2 - x1)
            c = y1 - (slope * x1)
        return slope, c
    

    @staticmethod 
    def Shape_outline(Blockref_Points, all_walls, insert_refs):
        #This function Filters the Block References and Points to ensure any unwanted Points are not picked up 
        filtered_blockref = []
        filtered_insert_refs = []  # ← NEW: Store filtered refs

        for idx, block in enumerate(Blockref_Points):
            name = block[0]
            x = block[1]
            y = block[2]
            angle = block[3]
            name_error = block[4]
        
            if 10 <= x <= 300000 and 10 <= y <= 300000: 
                filtered_blockref.append([name, x, y, angle, name_error])
                filtered_insert_refs.append(insert_refs[idx])  # ← Filter refs too
        
        all_x = []
        all_y = []

        for _, x, y, _, _ in filtered_blockref:
            all_x.append(x)
            all_y.append(y)

        filtered_walls = []
        for wall in all_walls: 
            for point in wall:
                x, y = point[0], point[1]
                if 10 <= x <= 300000 and 10 <= y <= 300000:
                    all_x.append(x)
                    all_y.append(y)
                    filtered_walls.append([x, y])

        return filtered_blockref, filtered_walls, filtered_insert_refs  

    @staticmethod
    def find_distance_to_line(x_point, y_point, slope, intercept):
        if slope is None:
            x_intercept = float(intercept.split()[2])
            return abs(x_point - x_intercept)
        else:
            return abs(y_point - (slope * x_point + intercept))

    @staticmethod
    def solve_simultaneous_equations(closest_slope, closest_intercept, slope_line, intercept_line):
        x, y = symbols('x y')
        eq1 = Eq(y, closest_slope * x + closest_intercept)
        eq2 = Eq(y, slope_line * x + intercept_line)
        solution = solve((eq1, eq2), (x, y))
        return float(solution[x]), float(solution[y])