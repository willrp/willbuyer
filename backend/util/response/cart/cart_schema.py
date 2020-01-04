from marshmallow import Schema, fields

from .models.price import PriceSchema
from .models.product import ProductSchema


class CartSchema(Schema):
    products = fields.Nested(ProductSchema, required=True, many=True)
    total = fields.Nested(PriceSchema, required=True)
