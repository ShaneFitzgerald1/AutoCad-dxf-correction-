from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine(
    'postgresql+psycopg2://postgres:Rodney2004@localhost:5432/objectdatabase',
    echo=False  # Set to True temporarily if you want to debug SQL queries
)

Base = declarative_base()

class ObjectID(Base):
    __tablename__ = 'objects'
    object_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    category = Column(String)
    on_channel_outline = Column(String)

    def __repr__(self):
        return f"<ObjectID(name={self.name}, type={self.type}, on_channel_outline={self.on_channel_outline})>"

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)