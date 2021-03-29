from marshmallow import Schema, fields


class ToolSchema:
    id = fields.Int(required=True)
    ip = fields.Str(required=True)
    port = fields.Int(required=True)
    git = fields.URL()
    input_specs_schema = fields.Str()
    input_specs_schema = fields.Str()
    input_specs_schema = fields.Str()
    output_specs = fields.Str()
    author_specs = fields.Str()
    name = fields.Str()
    enum = fields.Str()
