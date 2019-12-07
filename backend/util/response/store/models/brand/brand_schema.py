from marshmallow import Schema, fields


class BrandSchema(Schema):
    brand = fields.String(required=True)
    amount = fields.Integer(required=True)
