from marshmallow import Schema, fields


class KindSchema(Schema):
    kind = fields.String(required=True)
    amount = fields.Integer(required=True)
