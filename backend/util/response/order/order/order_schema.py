from marshmallow import Schema, fields, EXCLUDE

from ..models.price import PriceSchema
from ..models.product import ProductSchema


class OrderSchema(Schema):
    slug = fields.String(required=True)
    user_slug = fields.String(required=True)
    product_types = fields.Integer(required=True)
    items_amount = fields.Integer(required=True)
    total = fields.Nested(PriceSchema, required=True)
    products = fields.List(fields.Nested(ProductSchema, required=True), required=True)
    updated_at = fields.String(required=True)

    class Meta:
        unknown = EXCLUDE
