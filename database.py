import os

from marshmallow import Schema, fields, pre_load
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "tmp/notes.db"))

# engine = create_engine('sqlite:///:memory:', convert_unicode=True)
engine = create_engine(database_file, convert_unicode=True)

Session = sessionmaker(autocommit=False,
                       bind=engine)

Base = declarative_base()


class Note(Base):
    __tablename__ = 'notes'

    id = Column(String(36), primary_key=True)
    title = Column(String(30))
    text = Column(String(500))
    date_create = Column(Integer)
    date_update = Column(Integer)

    def __repr__(self):
        return "<Note (id='%s', title='%s', text='%s', date_create='%d', date_update='%d')>" % (
            self.id, self.title, self.text, self.date_create, self.date_update)


def init_db():
    Base.metadata.bind = engine
    Base.metadata.create_all()


def empty_db():
    """
    Empties a local database.
    """
    db_session = Session()
    db_session.query(Note).delete()
    db_session.commit()
    db_session.close()


##### SCHEMAS #####


class NoteSchema(Schema):
    id = fields.Str()
    title = fields.Str()
    text = fields.Str()
    date_create = fields.Int(dump_only=True)
    date_update = fields.Int(dump_only=True)

    @pre_load
    def encode(self, data):
        if data.get('title'):
            data['title'] = data['title'].encode("utf-8", "surrogateescape")
        else:
            data['title'] = {}

        if data.get('text'):
            data['text'] = data['text'].encode("utf-8", "surrogateescape")
        else:
            data['text'] = {}
        return data


note_schema = NoteSchema()
notes_schema = NoteSchema(many=True)
