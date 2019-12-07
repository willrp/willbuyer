from marshmallow import Schema, fields


class PriceSchema(Schema):
    outlet = fields.Float(required=True)
    retail = fields.Float(required=True)
    symbol = fields.String(required=True)
