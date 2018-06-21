from marshmallow import Schema, fields, pre_load


class NoteSchema(Schema):
    id = fields.UUID()
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
