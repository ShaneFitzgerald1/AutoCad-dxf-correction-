import sys
import os
import shutil
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class ObjectID(Base):
    __tablename__ = 'objects'
    object_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    category = Column(String)
    on_channel_outline = Column(String)

class CategoryLineRule(Base):
    __tablename__ = 'category_line_rules'
    id = Column(Integer, primary_key=True)
    category = Column(String, nullable=False)
    allowed_connections = Column(String)
    double_connection = Column(String, nullable=False)

def get_db_path():
    app_data = os.path.join(os.environ.get('APPDATA', os.path.expanduser('~')), 'MJHInterface')
    os.makedirs(app_data, exist_ok=True)
    
    user_db = os.path.join(app_data, 'objectdatabase.db')
    
    if not os.path.exists(user_db):
        if getattr(sys, 'frozen', False):
            bundled_db = os.path.join(sys._MEIPASS, 'objectdatabase.db')
        else:
            bundled_db = os.path.join(os.path.dirname(__file__), '..', 'objectdatabase.db')
        
        if os.path.exists(bundled_db):
            shutil.copy2(bundled_db, user_db)
        else:
            engine_temp = create_engine(f'sqlite:///{user_db}', echo=False)
            Base.metadata.create_all(engine_temp)
            return user_db
    
    return user_db

engine = create_engine(f'sqlite:///{get_db_path()}', echo=False)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)