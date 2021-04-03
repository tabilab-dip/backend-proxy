from marshmallow import Schema, fields


class ToolSchema(Schema):
    _id = fields.Int(required=True)
    ip = fields.Str(required=True)
    port = fields.Int(required=True)
    git = fields.Str(required=True)
    name = fields.Str(required=True)
    # enum needs to be unique
    enum = fields.Str(required=True)
    author_json = fields.Str(required=True)  # ~~
    root_json = fields.Str(required=True)  # ~~
    form_data_json = fields.Str(required=True)  # ~~
