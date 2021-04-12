from marshmallow import Schema, fields


class UserSchema(Schema):
    _id = fields.Int(required=True)
    username = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True)
    roles = fields.List(fields.String(), required=True)
