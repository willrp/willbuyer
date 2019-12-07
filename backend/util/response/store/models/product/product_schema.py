from marshmallow import Schema, fields

from ..price import PriceSchema


class ProductSchema(Schema):
    id = fields.String(required=True)
    name = fields.String(required=True)
    image = fields.String(required=True)
    price = fields.Nested(PriceSchema, required=True)
    discount = fields.Integer(required=True)
