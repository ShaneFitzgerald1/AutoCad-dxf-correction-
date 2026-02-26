"""
db_seed.py
----------
Run this script ONCE to populate the database with known object types.
Do NOT import this file anywhere in your main application.

Usage:
    python -m database.db_seed
"""

from database.db_models import Session, ObjectID

objects_data = [
    {'name': 'CPSHS100X100X8',     'type': 'INSERT', 'category': 'CP',     'on_channel_outline': 'Yes'},
    {'name': 'CPSHS120X120X6',     'type': 'INSERT', 'category': 'CP',     'on_channel_outline': 'Yes'},
    {'name': 'CPSHS120X120X6-B',   'type': 'INSERT', 'category': 'CP',     'on_channel_outline': 'Yes'},
    {'name': 'CPSHS150X50X8',      'type': 'INSERT', 'category': 'CP',     'on_channel_outline': 'Yes'},
    {'name': 'CPSHS150X50X8-B',    'type': 'INSERT', 'category': 'CP',     'on_channel_outline': 'Yes'},
    {'name': 'CPSHS160X160X16',    'type': 'INSERT', 'category': 'CP',     'on_channel_outline': 'Yes'},
    {'name': 'CPSHS160X160X16-B',  'type': 'INSERT', 'category': 'CP',     'on_channel_outline': 'Yes'},
    {'name': 'CPSHS180X180X16',    'type': 'INSERT', 'category': 'CP',     'on_channel_outline': 'Yes'},
    {'name': 'CPSHS180X180X16-B',  'type': 'INSERT', 'category': 'CP',     'on_channel_outline': 'Yes'},
    {'name': 'CPSHS150X50X8-L',    'type': 'INSERT', 'category': 'CP',     'on_channel_outline': 'Yes'},
    {'name': 'CPSHS150X50X8-PLATE','type': 'INSERT', 'category': 'CP',     'on_channel_outline': 'Yes'},
    {'name': 'CPRHS140X120X12.5',  'type': 'INSERT', 'category': 'CP',     'on_channel_outline': 'Yes'},
    {'name': 'CPSHS150x150x8','type': 'INSERT', 'category': 'CP',     'on_channel_outline': 'Yes'},
    {'name': 'CPSHS150x150x8-B',  'type': 'INSERT', 'category': 'CP',     'on_channel_outline': 'Yes'},

    {'name': 'NLB 30 CENTRE',      'type': 'INSERT', 'category': 'STUD',   'on_channel_outline': 'Yes'},
    {'name': 'NLB 50 CENTRE',      'type': 'INSERT', 'category': 'STUD',   'on_channel_outline': 'Yes'},
    {'name': 'NLB 60 CENTRE',      'type': 'INSERT', 'category': 'STUD',   'on_channel_outline': 'Yes'},
    {'name': 'NLB CORNER 50',      'type': 'INSERT', 'category': 'STUD',   'on_channel_outline': 'Yes'},
    {'name': 'NLB CORNER 60',      'type': 'INSERT', 'category': 'STUD',   'on_channel_outline': 'Yes'},

    {'name': 'MV01',               'type': 'INSERT', 'category': 'CONN',   'on_channel_outline': 'Yes'},
    {'name': 'SF01-150-A',         'type': 'INSERT', 'category': 'CONN',   'on_channel_outline': 'Yes'},
    {'name': 'SF01-150-B',         'type': 'INSERT', 'category': 'CONN',   'on_channel_outline': 'Yes'},
    {'name': 'SF01-180-A',         'type': 'INSERT', 'category': 'CONN',   'on_channel_outline': 'Yes'},
    {'name': 'SF01-180-N',         'type': 'INSERT', 'category': 'CONN',   'on_channel_outline': 'Yes'},
    {'name': 'SF01-150-N',         'type': 'INSERT', 'category': 'CONN',   'on_channel_outline': 'Yes'},
    {'name': 'SF03-150-A',         'type': 'INSERT', 'category': 'CONN',   'on_channel_outline': 'Yes'},
    {'name': 'SF03-150-N',         'type': 'INSERT', 'category': 'CONN',   'on_channel_outline': 'Yes'},
    {'name': 'SF03-180-A',         'type': 'INSERT', 'category': 'CONN',   'on_channel_outline': 'Yes'},
    {'name': 'SF03-180-N',         'type': 'INSERT', 'category': 'CONN',   'on_channel_outline': 'Yes'},
    {'name': 'SF-15',              'type': 'INSERT', 'category': 'CONN',   'on_channel_outline': 'Yes'},
    {'name': 'SF-15-OPP',          'type': 'INSERT', 'category': 'CONN',   'on_channel_outline': 'Yes'},
    {'name': 'VT1',                'type': 'INSERT', 'category': 'CONN',   'on_channel_outline': 'Yes'},
    {'name': 'MV02',               'type': 'INSERT', 'category': 'CONN',   'on_channel_outline': 'Yes'},
    {'name': 'SF-16',              'type': 'INSERT', 'category': 'CONN',   'on_channel_outline': 'Yes'},

    {'name': 'B1',                 'type': 'INSERT', 'category': 'OTHER',  'on_channel_outline': 'Yes'},
    {'name': 'B2',                 'type': 'INSERT', 'category': 'OTHER',  'on_channel_outline': 'Yes'},
    {'name': 'B3',                 'type': 'INSERT', 'category': 'OTHER',  'on_channel_outline': 'Yes'},
    {'name': 'B4',                 'type': 'INSERT', 'category': 'OTHER',  'on_channel_outline': 'Yes'},
    {'name': 'B5',                 'type': 'INSERT', 'category': 'OTHER',  'on_channel_outline': 'Yes'},
    {'name': 'B6',                 'type': 'INSERT', 'category': 'OTHER',  'on_channel_outline': 'Yes'},
    {'name': 'LP',                 'type': 'INSERT', 'category': 'OTHER',  'on_channel_outline': 'Yes'},
    {'name': 'NP',                 'type': 'INSERT', 'category': 'OTHER',  'on_channel_outline': 'Yes'},
    {'name': 'TRUSS VERTICAL',     'type': 'INSERT', 'category': 'OTHER',  'on_channel_outline': 'No'},
    {'name': 'RESTRAINT',          'type': 'INSERT', 'category': 'OTHER',  'on_channel_outline': 'Yes'},
    {'name': 'STIFFENER',          'type': 'INSERT', 'category': 'OTHER',  'on_channel_outline': 'Yes'},
    {'name': 'COUPLER',            'type': 'INSERT', 'category': 'OTHER',  'on_channel_outline': 'Yes'},

    {'name': 'WINDOW 1',           'type': 'INSERT', 'category': 'WINDOW', 'on_channel_outline': 'Yes'},
    {'name': 'WINDOW 2',           'type': 'INSERT', 'category': 'WINDOW', 'on_channel_outline': 'Yes'},
    {'name': 'WINDOW 3',           'type': 'INSERT', 'category': 'WINDOW', 'on_channel_outline': 'Yes'},
    {'name': 'WINDOW 4',           'type': 'INSERT', 'category': 'WINDOW', 'on_channel_outline': 'Yes'},
    {'name': 'WINDOW 5',           'type': 'INSERT', 'category': 'WINDOW', 'on_channel_outline': 'Yes'},

    {'name': 'CENTER',             'type': 'INSERT', 'category': 'WP',     'on_channel_outline': 'Yes'},
    {'name': 'CORNER',             'type': 'INSERT', 'category': 'WP',     'on_channel_outline': 'Yes'},
    {'name': 'LEFT',               'type': 'INSERT', 'category': 'WP',     'on_channel_outline': 'Yes'},
    {'name': 'RIGHT',              'type': 'INSERT', 'category': 'WP',     'on_channel_outline': 'Yes'},
    {'name': 'NLB CENTER',         'type': 'INSERT', 'category': 'WP',     'on_channel_outline': 'Yes'},
    {'name': 'NLB LEFT',           'type': 'INSERT', 'category': 'WP',     'on_channel_outline': 'Yes'},
    {'name': 'NLB RIGHT',          'type': 'INSERT', 'category': 'WP',     'on_channel_outline': 'Yes'},
    {'name': 'NARROW LEFT',        'type': 'INSERT', 'category': 'WP',     'on_channel_outline': 'Yes'},
    {'name': 'NARROW RIGHT',       'type': 'INSERT', 'category': 'WP',     'on_channel_outline': 'Yes'},
    {'name': 'DEFINITE NARROW LEFT','type': 'INSERT','category': 'WP',     'on_channel_outline': 'Yes'},
    {'name': 'DEFINITE NARROW RIGHT','type':'INSERT','category': 'WP',     'on_channel_outline': 'Yes'},
    {'name': 'CORNER-M',           'type': 'INSERT', 'category': 'WP',     'on_channel_outline': 'Yes'},

    {'name': '535 TRUSS LINE',     'type': 'LINE',   'category': 'TRUSS',  'on_channel_outline': 'No'},
    {'name': '460 TRUSS LINE',     'type': 'LINE',   'category': 'TRUSS',  'on_channel_outline': 'No'},
    {'name': '475 TRUSS LINE',     'type': 'LINE',   'category': 'TRUSS',  'on_channel_outline': 'No'},
    {'name': '275 TRUSS LINE',     'type': 'LINE',   'category': 'TRUSS',  'on_channel_outline': 'No'},
    {'name': 'TRUSS BRACING',      'type': 'LINE',   'category': 'TRUSS',  'on_channel_outline': 'No'},
    {'name': '325 TRUSS LINE',     'type': 'LINE',   'category': 'TRUSS',  'on_channel_outline': 'No'},
    {'name': '225 TRUSS LINE',     'type': 'LINE',   'category': 'TRUSS',  'on_channel_outline': 'No'},
    {'name': '60 SHS TRUSS LINE',  'type': 'LINE',   'category': 'TRUSS',  'on_channel_outline': 'No'},

    {'name': '80 HEADER',          'type': 'LINE',   'category': 'HEADER', 'on_channel_outline': 'Yes'},
    {'name': '60 HEADER',          'type': 'LINE',   'category': 'HEADER', 'on_channel_outline': 'Yes'},
    {'name': '40 HEADER',          'type': 'LINE',   'category': 'HEADER', 'on_channel_outline': 'Yes'},

    {'name': '350 CILL',           'type': 'LINE',   'category': 'OTHER',  'on_channel_outline': 'Yes'},
    {'name': 'WALL',               'type': 'LINE',   'category': 'OTHER',  'on_channel_outline': 'Yes'},

    {'name': 'Door',               'type': 'LWPOLYLINE', 'category': None, 'on_channel_outline': 'No'},
]

def seed_database():
    session = Session()
    try:
        existing_count = session.query(ObjectID).count()
        if existing_count > 0:
            print(f"Database already has {existing_count} objects. Skipping seed to avoid duplicates.")
            print("If you want to re-seed, clear the objects table first.")
            return

        objects = [ObjectID(**data) for data in objects_data]
        session.add_all(objects)
        session.commit()
        print(f"Successfully seeded {len(objects)} objects into the database.")
    except Exception as e:
        session.rollback()
        print(f"Seeding failed: {e}")
        raise
    finally:
        session.close()

if __name__ == '__main__':
    seed_database()
