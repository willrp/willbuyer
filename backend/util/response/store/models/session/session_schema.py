from marshmallow import Schema, fields


class SessionSchema(Schema):
    id = fields.String(required=True)
    name = fields.String(required=True)
    gender = fields.String(required=True)
    image = fields.String(required=True)
    total = fields.Integer(required=True)
