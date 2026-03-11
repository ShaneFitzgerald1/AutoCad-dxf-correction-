from database.db_models import Session, ObjectID, CategoryLineRule
from backend.mathematical import Mathematical
maths = Mathematical()

def get_catalogue():

    objects = []
    session = Session()
    try:
        all_objects = session.query(ObjectID).all()
        for obj in all_objects:
            objects.append([obj.name, obj.type, obj.category, obj.on_channel_outline ])
        return objects
    except Exception as e:
        print(f"Warning: Could not load catalogue from database: {e}")
        return [] 
    finally:
        session.close()

def get_category_catalogue(): 

    categories = []
    session = Session() 
    try:
        all_categories = session.query(CategoryLineRule).all()
        for cat in all_categories:
            categories.append([cat.category, cat.allowed_connections, cat.double_connection ])
        return categories
    
    except Exception as e:
        print(f"Warning: Could not load catalogue from database: {e}")
        return [] 
    finally:
        session.close()   

# categories = get_category_catalogue() 
# print(f'These are the categories {categories}')

       


def name_match_block(blockrefs, lines, actual_type, wall_slopes, wall_intercepts, all_walls, line_refs): 
    blocks = maths.Channel_check_block(wall_slopes, wall_intercepts, blockrefs)

    _, _, _, _, lines_cl = maths.Chanel_check_line(wall_slopes, wall_intercepts, lines, all_walls, line_refs)
    objects = get_catalogue()
    accepted_block_names = []
    rejected_block_names = []
    accepted_line_names = []
    rejected_line_names = []


    # Build lookup lists from catalogue
    valid_insert_names = []
    valid_line_names = []

    # print(f'These are the objects{objects}')
    # print(f'Amount of objects {len(objects)}')

    for object in objects:
        name, type, category, on_channel_outline = object
        if type not in ('LINE', 'LWPOLYLINE'):
            valid_insert_names.append((name, on_channel_outline))
        if type not in ('INSERT', 'LWPOLYLINE'):
            valid_line_names.append((name, on_channel_outline))

    if actual_type == 'INSERT':
        for block in blocks:
            actual_name, x, y, _, on_channel = block
            matched = False
            channel_verification = False

            for name, on_channel_outline in valid_insert_names:
                if actual_name.upper() == name.upper():
                    matched = True
                    if on_channel == 'Yes' and on_channel_outline == 'Yes':
                        channel_verification = True
                    if on_channel == 'No' and on_channel_outline == 'No':
                        channel_verification = True
                    break

            if matched and channel_verification:
                accepted_block_names.append(actual_name)
            if matched and not channel_verification:
                rejected_block_names.append([actual_name, x, y, 'Block rejected due to unexpected position'])
            if not matched and channel_verification:
                rejected_block_names.append([actual_name, x, y, 'Block has unexpected name'])
            if not matched and not channel_verification:
                rejected_block_names.append([actual_name, x, y, 'Block rejected due to unexpected position and name'])

        return accepted_block_names, rejected_block_names

    if actual_type == 'LINE':
        for line in lines_cl:
            actual_l_name, x_s, y_s, x_e, y_e, on_channel = line
            line_matched = False
            channel_verified = False

            for name, on_channel_outline in valid_line_names:
                if actual_l_name.upper() == name.upper():
                    line_matched = True
                    if on_channel == 'Yes' and on_channel_outline == 'Yes':
                        channel_verified = True
                    if on_channel == 'No' and on_channel_outline == 'No':
                        channel_verified = True
                    break

            if line_matched and channel_verified:
                accepted_line_names.append(actual_l_name)
            if line_matched and not channel_verified:
                rejected_line_names.append([actual_l_name, x_s, y_s, x_e, y_e, 'Line rejected due to not being in expected position'])
            if not line_matched and not channel_verified:
                rejected_line_names.append([actual_l_name, x_s, y_s, x_e, y_e, f'Line rejected: {actual_l_name} is not present in the DataBase'])

        return accepted_line_names, rejected_line_names
    

def before_after(fixed_all_blocks, blockrefs, lines, correct_lines, fixed_lines, wall_slopes, wall_intercepts, all_walls, line_refs):
        
    # correct_lines.extend(fixed_lines)
    all_correct_lines = correct_lines + fixed_lines

    sort_blockrefs = []
    
    for block in blockrefs: #sorting blockrefs 
        name, x, y, angle, name_error = block 
        if name_error is not None: 
            sort_blockrefs.append([name_error, x, y, angle, name])
        else:
            sort_blockrefs.append([name, x, y, angle, name_error])    

    #These are all the accepted blocks and lines before they are passed through the correction code 
    initial_accepted_blocks, initial_rejected_blocks = name_match_block(sort_blockrefs, lines, 'INSERT', wall_slopes, wall_intercepts, all_walls, line_refs)
    initial_accepted_line, initial_rejected_lines = name_match_block(sort_blockrefs, lines, 'LINE', wall_slopes, wall_intercepts, all_walls, line_refs)

    #All accepted and rejected blocks post check, if an error arised here this is a big issue
    post_accepted_block, post_rejected_block = name_match_block(fixed_all_blocks, all_correct_lines, 'INSERT', wall_slopes, wall_intercepts, all_walls, line_refs)
    post_accepted_line, post_rejected_lines = name_match_block(fixed_all_blocks, all_correct_lines, 'LINE', wall_slopes, wall_intercepts, all_walls, line_refs)

    print(f'There are initially {len(initial_accepted_blocks)} Accepted Blocks and {len(initial_rejected_blocks)} Rejected Blocks from the object DataBase  ')
    for block in initial_rejected_blocks: 
        name, x, y, rejection_reason = block 
        print(f'Block: {(name), (x), (y)}: {rejection_reason}')

    print(f'There are initially {len(initial_accepted_line)} Accepted Lines and {len(initial_rejected_lines)} Rejected Lines from the object DataBase')
    for line in initial_rejected_lines: 
        name, xs, ys, xe, ye, rejection_reason = line 
        print(f'Line: {(name), (xs), (ys), (xe), (ye)}: {rejection_reason}')

    print(f'Post correction there are {len(post_accepted_block)} Accepted Blocks and {len(post_rejected_block)} Rejected Blocks from the obejct Database ')    
    for block in post_rejected_block: 
        name, x, y, rejection_reason = block 
        print(f'Block: {(name), (x), (y)}: {rejection_reason}')

    print(f'Post correction there are {len(post_accepted_line)} Accepted Lines and {len(post_rejected_lines)} Rejected Lines from the object Database')
    for line in post_rejected_lines: 
        name, xs, ys, xe, ye, rejection_reason = line 
        print(f'Line: {(name), (xs), (ys), (xe), (ye)}: {rejection_reason}')   


    return post_accepted_block, post_accepted_line, post_rejected_block, post_rejected_lines 



def categories_sorter(line_connections): 
    category_list = [] 

    for line in line_connections: 
        line_name, line_start_entity, line_end_entity, x_start, y_start, x_end, y_end = line 

        line_category = get_category(line_name)
        line_start_category = get_category(line_start_entity)
        line_end_category = get_category(line_end_entity)

        category_list.append([line_name, line_category, line_start_category, line_end_category, x_start, y_start, x_end, y_end])

    return category_list     

    
def get_category(line_name): 
    """Function that puts each line name into a category based on its name"""
    objects = get_catalogue()
    if line_name is None: 
        return None 
    for object in objects: 
        object_name, type, category, on_channel_outline = object 
        if line_name.upper() == object_name.upper(): 
            return category 
    return None 


def validate_categories(line_line_connections, line_block_connections):
    categories = get_category_catalogue() 

    ll_connections = categories_sorter(line_line_connections)
    lb_connections = categories_sorter(line_block_connections)
    all_connections = ll_connections + lb_connections
    correct_connections_cat = []
    mand_fail = []
    quantity_fail = []
    both_fail = []

    for line in all_connections: 
        line_name, line_category, line_start_category, line_end_category, x_start, y_start, x_end, y_end = line 
        safe_connections = False 
        untrue_quantity_connections = False 

        for categor in categories: 
            cat, allowed_connections, double_connection = categor

            if allowed_connections:
                allowed_list = [a.strip() for a in allowed_connections.split(',')]
            else:
                allowed_list = [] 

            if cat == line_category: 
                if line_start_category in allowed_list and line_end_category in allowed_list:  
                    safe_connections = True 
                
                if line_category == 'TRUSS LINE': 
                    if line_start_category is None or line_end_category is None: 
                        safe_connections = True  
                    if line_start_category == 'TRUSS BRACING' or line_end_category == 'TRUSS BRACING': 
                        safe_connections = True 
                    if line_start_category == 'TRUSS BRACING' and line_end_category == 'TRUSS BRACING': 
                        safe_connections = False   

                if line_category == 'SHS TRUSS LINE': 
                    if line_start_category is None or line_end_category is None: 
                        safe_connections = True          

                if double_connection == 'Yes': 
                    if line_category == 'TRUSS LINE' or line_category == 'SHS TRUSS LINE': 
                        continue 
                    if line_start_category is None or line_end_category is None: 
                        untrue_quantity_connections = True 

                if cat == 'BRACE LINE':  #brace lines may fall short of studs 
                    if line_start_category == 'CP' and line_end_category is None:
                        safe_connections = True 
                        untrue_quantity_connections = False 
                    if line_end_category == 'CP' and line_start_category is None: 
                        safe_connections = True       
                        untrue_quantity_connections = False       
       

        if safe_connections and not untrue_quantity_connections: 
            correct_connections_cat.append([line_name])  
        if not safe_connections and not untrue_quantity_connections: 
            mand_fail.append([line_name, x_start, y_start, line_start_category, x_end, y_end, line_end_category, 'Line starts or ends on an incorrect line, object, or position.'])
        if safe_connections and untrue_quantity_connections: 
            quantity_fail.append([line_name, x_start, y_start, line_start_category, x_end, y_end, line_end_category, 'Line must end on the specified object.'])
        if not safe_connections and untrue_quantity_connections: 
            both_fail.append([line_name, x_start, y_start, line_start_category, x_end, y_end, line_end_category, 'Line start/end is incorrect or does not end on the required object.'])

    print(f'{len(correct_connections_cat)} Lines were approved by the Category DataBase')
    print(f'{len(mand_fail)} Lines were disapproved due to lines ending on incorrect lines/objects')
    print(f'These are the mand fail lines {mand_fail}')
    print(f'{len(quantity_fail)} Lines were disapproved due to lines not ending on lines/objects')
    print(f'{len(both_fail)} Lines were disapproved due to lines not ending on lines/objects and ending on incorrect object')
    print(f'Both failed lines is {both_fail}')

    all_fail_cat = mand_fail + quantity_fail + both_fail 

    return correct_connections_cat, all_fail_cat

    








        




# def add_new_object(name, obj_type, category, on_channel_outline):
#     session = Session() 
#     new_obj = ObjectID(name=name,
#             type=obj_type,
#             category=category,
#             on_channel_outline=on_channel_outline) 
#     session.add(new_obj)
#     session.commit()
#     session.close() 

# add_new_object('205 TRUSS LINE', 'LINE', 'TRUSS LINE', 'No')

# add_new_object('305 TRUSS LINE', 'LINE', 'TRUSS LINE', 'No')


# add_new_object('CPSHS150x150x8-L', 'INSERT', 'CP', 'Yes' )   
         

    
# def remove_object(name):
#     session = Session()
#     obj = session.query(ObjectID).filter_by(name=name).first()
#     if obj:
#         session.delete(obj)
#         session.commit()
#         print(f"Removed: {name}")
#     else:
#         print(f"Not found: {name}")
#     session.close()

# remove_object('60 SHS TRUSS LINE')    

# remove_object('215 TRUSS LINE')
# remove_object('205 TRUSS LINE')
            











# def add_new_object(category, allowed_connections, double_connection):
#     session = Session() 
#     new_obj = CategoryLineRule(
#             category=category,
#             allowed_connections=str(allowed_connections),
#             double_connection=double_connection) 
#     session.add(new_obj)
#     session.commit()
#     session.close()

# add_new_object('TRUSS BRACING', ('TRUSS LINE' , 'HEADER', 'WALL LINE', 'CILL LINE', 'BRACE LINE') , 'Yes' )  

    
# def remove_object(name):
#     session = Session()
#     obj = session.query(CategoryLineRule).filter_by(category = name).first()
#     if obj:
#         session.delete(obj)
#         session.commit()
#         print(f"Removed: {name}")
#     else:
#         print(f"Not found: {name}")
#     session.close()

# remove_object('TRUSS BRACING')
