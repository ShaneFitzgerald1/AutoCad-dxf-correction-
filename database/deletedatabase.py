import os

def reset_database():
    # Delete user db
    app_data = os.path.join(os.environ.get('APPDATA', os.path.expanduser('~')), 'MJHInterface')
    user_db = os.path.join(app_data, 'objectdatabase.db')
    if os.path.exists(user_db):
        os.remove(user_db)
        print(f"Deleted user db: {user_db}")

    # Delete bundled db too
    bundled_db = os.path.join(os.path.dirname(__file__), '..', 'objectdatabase.db')
    bundled_db = os.path.normpath(bundled_db)
    if os.path.exists(bundled_db):
        os.remove(bundled_db)
        print(f"Deleted bundled db: {bundled_db}")

if __name__ == '__main__':
    reset_database()