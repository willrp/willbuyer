from marshmallow import Schema, fields


class PriceRangeSchema(Schema):
    min = fields.Float(required=True)
    max = fields.Float(required=True)
