from marshmallow import Schema, fields

from ..models.order_min import OrderMinSchema


class UserOrdersSchema(Schema):
    orders = fields.Nested(OrderMinSchema, required=True, many=True)
    total = fields.Integer(required=True)
    pages = fields.Integer(required=True)
