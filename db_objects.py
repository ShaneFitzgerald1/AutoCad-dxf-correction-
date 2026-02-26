"""
db_queries.py
-------------
All database query and write functions used by the main application.
Import this file wherever database access is needed.

Main functions:
    get_catalogue()         - Load all known objects into a lookup dictionary (call once on file import)
    add_new_object()        - Add a newly accepted unknown object to the database
    object_exists()         - Check if a single name exists in the database
"""

from database.db_models import Session, ObjectID
from backend.mathematical import Mathematical
maths = Mathematical()

def get_catalogue():

    objects = []
    session = Session()
    try:
        all_objects = session.query(ObjectID).all()
        for obj in all_objects:
            objects.append([obj.name, obj.type, obj.category, obj.on_channel_outline ])
 
        # print(f"Catalogue loaded: {len(objects)} known objects from database.")
        return objects
    except Exception as e:
        print(f"Warning: Could not load catalogue from database: {e}")
        return [] 
    finally:
        session.close()


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
                if actual_name == name:
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
                if actual_l_name == name:
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
            if not line_matched and channel_verified:
                rejected_line_names.append([actual_l_name, x_s, y_s, x_e, y_e,'Unexpected Line name'])
            if not line_matched and not channel_verified:
                rejected_line_names.append([actual_l_name, x_s, y_s, x_e, y_e, 'Line rejected due to unexpected position and Line name'])

        return accepted_line_names, rejected_line_names
    

def before_after(fixed_all_blocks, blockrefs, lines, correct_lines, fixed_lines, wall_slopes, wall_intercepts, all_walls, line_refs):
        
    correct_lines.extend(fixed_lines)
    all_lines_fixed = idk 
    print(f'These are all lines fixed {correct_lines}')
    print(f'Total correct lines {len(correct_lines)}')
    print(f'Total lines {len(lines)}')


    #These are all the accepted blocks and lines before they are passed through the correction code 
    initial_accepted_blocks, initial_rejected_blocks = name_match_block(blockrefs, lines, 'INSERT', wall_slopes, wall_intercepts, all_walls, line_refs)
    initial_accepted_line, initial_rejected_lines = name_match_block(blockrefs, lines, 'LINE', wall_slopes, wall_intercepts, all_walls, line_refs)

    #All accepted and rejected blocks post check, if an error arised here this is a big issue
    post_accepted_block, post_rejected_block = name_match_block(fixed_all_blocks, lines, 'INSERT', wall_slopes, wall_intercepts, all_walls, line_refs)
    post_accepted_line, post_rejected_lines = name_match_block(fixed_all_blocks, lines, 'LINE', wall_slopes, wall_intercepts, all_walls, line_refs)

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

    print(f'Post correction there are {len(post_accepted_block)} Accepted Lines and {len(post_rejected_block)} Rejected Lines ')
    for line in post_rejected_lines: 
        name, xs, ys, xe, ye, rejection_reason = line 
        print(f'Line: {(name), (xs), (ys), (xe), (ye)}: {rejection_reason}')    




                

    





                




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