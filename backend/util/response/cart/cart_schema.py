from marshmallow import Schema, fields

from .item_schema import ItemSchema


class CartSchema(Schema):
    item_list = fields.Nested(ItemSchema, required=True, many=True)
