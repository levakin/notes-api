# -*- coding: utf-8 -*-
import time
import uuid

from flask import Flask, request
from flask_restplus import Resource, Api as BaseApi, fields
from marshmallow import ValidationError
from werkzeug.contrib.fixers import ProxyFix

import manage_db
from database import init_db, Session, empty_db, Note, notes_schema, note_schema


class Api(BaseApi):

    def _register_doc(self, app_or_blueprint):
        # HINT: This is just a copy of the original implementation with the last line commented out.
        if self._add_specs and self._doc:
            # Register documentation before root if enabled
            app_or_blueprint.add_url_rule(self._doc, 'doc', self.render_doc)
        # app_or_blueprint.add_url_rule(self._doc, 'root', self.render_root)

    @property
    def base_path(self):
        return ''


app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version='1.0',
          title='Notes API',
          description='Notes API',
          doc="/doc/",
          default="notes",
          default_label="Notes operations"
          )

note_post = api.model('post note', {
    'title': fields.String(example='title example'),
    'text': fields.String(example='text example')
})
note_update = api.model('update note', {
    'id': fields.String(example='91c947c7-3f24-47bc-b180-d36dadfaca1c'),
    'title': fields.String(example='title example'),
    'text': fields.String(example='text example')
})
note_delete = api.model('delete note', {
    'id': fields.String(example='91c947c7-3f24-47bc-b180-d36dadfaca1c')
})

init_db()


@app.cli.command()
def empty():
    empty_db()


@app.cli.command()
def add_examples():
    manage_db.test_reqs()


@app.cli.command()
def reset():
    empty_db()
    manage_db.test_reqs()


@api.route('/')
class NotesList(Resource):
    @api.doc('Get notes')
    def get(self):
        db_session = Session()
        notes = db_session.query(Note).all()
        result = notes_schema.dump(notes)
        db_session.close()
        return result

    @api.doc('Post note')
    @api.expect(note_post)
    @api.response(201, 'Note created')
    @api.response(400, 'No input data provided')
    @api.response(422, 'Data not provided')
    def post(self):

        json_data = request.get_json()

        if not json_data:
            return {'message': 'No input data provided'}, 400

        # Validate and deserialize input
        try:
            data, errors = note_schema.load(json_data)

            if not data.get('title') or not data.get('text'):
                raise ValidationError('Data not provided')

        except ValidationError as err:
            return err.messages, 422

        # Create new note
        note = Note(id=str(uuid.uuid4()),
                    title=data.get('title'),
                    text=data.get('text'),
                    date_create=int(time.time()),
                    date_update=int(time.time()))

        db_session = Session()
        db_session.add(note)
        db_session.commit()

        result, errors = note_schema.dump(db_session.query(Note).filter(Note.id == note.id).first())

        db_session.close()
        return result, 201

    @api.doc('Update note')
    @api.expect(note_update)
    @api.response(200, 'Note updated')
    @api.response(400, 'No input data provided')
    @api.response(422, 'Data not provided')
    @api.response(404, 'Note is not found')
    def put(self):
        db_session = Session()

        json_data = request.get_json()

        if not json_data:
            return {'message': 'No input data provided'}, 400

        # Validate and deserialize input
        try:
            data, errors = note_schema.load(json_data)
            if not (data.get('id') and (data.get('title') or data.get('text'))):
                raise ValidationError('Data not provided')

        except ValidationError as err:
            return err.messages, 422

        try:
            note = db_session.query(Note).filter(Note.id == data.get('id')).first()

            if note is None:
                raise ValidationError('Note is not found')

        except ValidationError as err:
            db_session.close()
            return err.messages, 404

        if data.get('title'):
            note.title = data.get('title')

        if data.get('text'):
            note.text = data.get('text')

        note.date_update = int(time.time())

        db_session.commit()

        result, errors = note_schema.dump(note)
        db_session.close()
        return result

    @api.doc('Delete note')
    @api.expect(note_delete)
    @api.response(200, 'Note successfully deleted')
    @api.response(400, 'No input data provided')
    @api.response(422, 'Data not provided')
    @api.response(404, 'Note is not found')
    def delete(self):
        db_session = Session()
        json_data = request.get_json()

        if not json_data:
            return {'message': 'No input data provided'}, 400

        try:
            data, errors = note_schema.load(json_data)
            if not data.get('id'):
                raise ValidationError('Data not provided')

        except ValidationError as err:
            db_session.close()
            return err.messages, 422

        try:
            note = db_session.query(Note).filter(Note.id == data.get('id')).first()
            if note is None:
                raise ValidationError('Note is not found')

        except ValidationError as err:
            db_session.close()
            return err.messages, 404

        db_session.delete(note)
        db_session.commit()
        db_session.close()

        return {"result": "Note successfully deleted"}


if __name__ == '__main__':
    app.run()
