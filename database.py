import os

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import UUIDType

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "tmp/notes.db"))

# engine = create_engine('sqlite:///:memory:', convert_unicode=True)
engine = create_engine(database_file, convert_unicode=True)

Session = sessionmaker(autocommit=False,
                       bind=engine)

Base = declarative_base()


class Note(Base):
    __tablename__ = 'notes'

    id = Column(UUIDType, primary_key=True, unique=True)
    title = Column(String(30))
    text = Column(String(500))
    date_create = Column(Integer)
    date_update = Column(Integer)

    def __repr__(self):
        return "<Note (id='%s', title='%s', text='%s', date_create='%d', date_update='%d')>" % (
            self.id, self.title, self.text, self.date_create, self.date_update)


def init_db():
    """
    Initialise a local database.
    """
    Base.metadata.bind = engine
    Base.metadata.create_all()


def empty_db():
    """
    Empties a local database.
    """
    if os.path.isfile('/tmp/notes.db'):
        os.remove('/tmp/notes.db')
    init_db()
