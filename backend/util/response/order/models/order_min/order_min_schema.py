from marshmallow import Schema, fields, EXCLUDE

from ..price.price_schema import PriceSchema


class OrderMinSchema(Schema):
    slug = fields.String(required=True)
    product_types = fields.Integer(required=True)
    items_amount = fields.Integer(required=True)
    total = fields.Nested(PriceSchema, required=True)
    updated_at = fields.String(required=True)

    class Meta:
        unknown = EXCLUDE
