from marshmallow import Schema, fields


class UserSchema(Schema):
    email = fields.Email(required=True)
    name = fields.String(required=True)
    picture = fields.URL(required=True)
