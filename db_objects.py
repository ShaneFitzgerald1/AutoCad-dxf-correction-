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

categories = get_category_catalogue() 
print(f'These are the categories {categories}')

       


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

    #These are all the accepted blocks and lines before they are passed through the correction code 
    initial_accepted_blocks, initial_rejected_blocks = name_match_block(blockrefs, lines, 'INSERT', wall_slopes, wall_intercepts, all_walls, line_refs)
    initial_accepted_line, initial_rejected_lines = name_match_block(blockrefs, lines, 'LINE', wall_slopes, wall_intercepts, all_walls, line_refs)

    #All accepted and rejected blocks post check, if an error arised here this is a big issue
    post_accepted_block, post_rejected_block = name_match_block(fixed_all_blocks, all_correct_lines, 'INSERT', wall_slopes, wall_intercepts, all_walls, line_refs)
    post_accepted_line, post_rejected_lines = name_match_block(fixed_all_blocks, all_correct_lines, 'LINE', wall_slopes, wall_intercepts, all_walls, line_refs)

    print(f'There are initially {len(initial_accepted_blocks)} Accepted Blocks and {len(initial_rejected_blocks)} Rejected Blocks ')
    for block in initial_rejected_blocks: 
        name, x, y, rejection_reason = block 
        print(f'Block: {(name), (x), (y)}: {rejection_reason}')

    print(f'There are initially {len(initial_accepted_line)} Accepted Lines and {len(initial_rejected_lines)} Rejected Lines ')
    for line in initial_rejected_lines: 
        name, xs, ys, xe, ye, rejection_reason = line 
        print(f'Line: {(name), (xs), (ys), (xe), (ye)}: {rejection_reason}')

    print(f'Post correction there are {len(post_accepted_block)} Accepted Blocks and {len(post_rejected_block)} Rejected Blocks ')    
    for block in post_rejected_block: 
        name, x, y, rejection_reason = block 
        print(f'Block: {(name), (x), (y)}: {rejection_reason}')

    print(f'Post correction there are {len(post_accepted_line)} Accepted Lines and {len(post_rejected_lines)} Rejected Lines ')
    for line in post_rejected_lines: 
        name, xs, ys, xe, ye, rejection_reason = line 
        print(f'Line: {(name), (xs), (ys), (xe), (ye)}: {rejection_reason}')    



def categories_sorter(line_connections): 
    category_list = [] 

    for line in line_connections: 
        line_name, line_start_entity, line_end_entity = line 

        line_category = get_category(line_name)
        line_start_category = get_category(line_start_entity)
        line_end_category = get_category(line_end_entity)

        category_list.append([line_name, line_category, line_start_category, line_end_category])

    return category_list     

    
def get_category(line_name): 
    objects = get_catalogue()
    for object in objects: 
        object_name, type, category, on_channel_outline = object 
        if line_name == object_name: 
            return category 
    return None 


def validate_categories(line_line_connections, line_block_connections):
    categories = get_category_catalogue() 
    ll_connections = categories_sorter(line_line_connections)
    lb_connections = categories_sorter(line_block_connections)
    all_connections = ll_connections + lb_connections
    correct_connections = []
    mand_fail = []
    quantity_fail = []
    both_fail = []

    for line in all_connections: 
        line_name, line_category, line_start_category, line_end_category = line 
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

                if double_connection == 'Yes': 
                    if line_start_category is None or line_end_category is None: 
                        untrue_quantity_connections = True 
                if double_connection == 'No': 
                    if line_start_category is not None and line_end_category is not None: 
                        untrue_quantity_connections = True    

        if safe_connections and not untrue_quantity_connections: 
            correct_connections.append([line_name])  
        if not safe_connections and not untrue_quantity_connections: 
            mand_fail.append([line_name])
        if safe_connections and untrue_quantity_connections: 
            quantity_fail.append([line_name])
        if not safe_connections and untrue_quantity_connections: 
            both_fail.append([line_name])

    print(f'{len(correct_connections)} were approved by the DataBase')
    print(f'{len(mand_fail)} were disapproved due to lines ending on incorrect lines/objects')
    print(f'{len(quantity_fail)} were disapproved due to lines not ending on lines/objects')
    print(f'{len(both_fail)} were disapproved due to lines not ending on lines/objects and ending on incorrect object')
    
    






                
                





def validate_category_database(line_line_connections, line_block_connections): 
    category_list_line = []
    category_list_block = []
    objects = get_catalogue()
    categories = get_category_catalogue() 

    for line in line_line_connections: 
        line_name, line_start_name, line_end_name = line 

        for object in objects: 
            name, type, category, on_channel_outline = object 
            if line_name == name: 
                category_list_line.append([line_name, line_start_name, line_end_name, category, on_channel_outline])

    for line in line_block_connections: 
        line_name, block_name_start, block_name_end = line 

        for object in objects: 
            name, type, category, on_channel_outline = object 
            if line_name == name: 
                category_list_block.append([line_name, block_name_start, block_name_end, category, on_channel_outline])       

    for line in category_list_line: 
        line_name, line_start_name, line_end_name, category, on_channel_outline = line 


        for categor in categories: 
            cat, allowed_connections, double_connection = categor

            if allowed_connections:
                allowed_list = [a.strip() for a in allowed_connections.split(',')]
            else:
                allowed_list = [] 

            if cat == category:  # ✅ now outside the else
                if line_start_name in allowed_list and line_end_name in allowed_list:  
                    print(f'{line_name} was verified')






        




# def add_new_object(name, obj_type, category, on_channel_outline):
#     session = Session() 
#     new_obj = ObjectID(name=name,
#             type=obj_type,
#             category=category,
#             on_channel_outline=on_channel_outline) 
#     session.add(new_obj)
#     session.commit()
#     session.close() 

# add_new_object('305 TRUSS LINE', 'LINE', 'TRUSS', 'No' )               

    
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

# remove_object('305 TRUSS LINE')
            




# def add_new_object(name, obj_type, category=None, on_channel_outline='Yes'):
#     """
#     Adds a new object to the database when a user accepts an unknown object via the GUI.

#     Args:
#         name (str):                 The block or layer name (e.g. 'NEW_BLOCK_TYPE')
#         obj_type (str):             'INSERT' or 'LINE'
#         category (str, optional):  Category grouping (e.g. 'CP', 'STUD'). None if unknown.
#         on_channel_outline (str):   'Yes' or 'No'

#     Returns:
#         True if successful, False if it failed (e.g. duplicate or DB error)
#     """
#     session = Session()
#     try:
#         # Guard against adding duplicates
#         existing = session.query(ObjectID).filter_by(name=name).first()
#         if existing:
#             print(f"Object '{name}' already exists in the database. Skipping.")
#             return False

#         new_obj = ObjectID(
#             name=name,
#             type=obj_type,
#             category=category,
#             on_channel_outline=on_channel_outline
#         )
#         session.add(new_obj)
#         session.commit()
#         print(f"New object '{name}' added to database successfully.")
#         return True
#     except Exception as e:
#         session.rollback()
#         print(f"Failed to add object '{name}' to database: {e}")
#         return False
#     finally:
#         session.close()


# def object_exists(name):
#     """
#     Quick check for whether a single name exists in the database.
#     Useful if you only need a yes/no without loading the whole catalogue.

#     Args:
#         name (str): The object name to check.

#     Returns:
#         True if found, False if not found or on DB error.
#     """
#     session = Session()
#     try:
#         result = session.query(ObjectID).filter_by(name=name).first()
#         return result is not None
#     except Exception as e:
#         print(f"Warning: Database check failed for '{name}': {e}")
#         return False
#     finally:
#         session.close()


# def validate_object(name, obj_type, catalogue):
#     """
#     Validates a single object name against the already-loaded catalogue dictionary.
#     Use this during DXF extraction rather than hitting the database per object.

#     Args:
#         name (str):         The object name to validate (block name or line layer name)
#         obj_type (str):     'INSERT' or 'LINE' - used to confirm it matches the expected type
#         catalogue (dict):   The dictionary returned by get_catalogue()

#     Returns a dict with:
#         {
#             'known':                True/False   - whether it exists in the database at all
#             'type_match':           True/False   - whether its DB type matches obj_type
#             'expected_on_outline':  'Yes'/'No'/None  - what the DB says about channel outline
#         }
#     """
#     if name not in catalogue:
#         return {
#             'known': False,
#             'type_match': False,
#             'expected_on_outline': None
#         }

#     db_entry = catalogue[name]
#     return {
#         'known': True,
#         'type_match': db_entry['type'] == obj_type,
#         'expected_on_outline': db_entry['on_channel_outline']
#     }