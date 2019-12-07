from flask_restplus import fields

from .cart_schema import CartSchema
from .item_response import ItemResponse


class CartResponse(object):
    @staticmethod
    def get_model(api, name):
        return api.model(
            name,
            {
                "item_list": fields.List(fields.Nested(ItemResponse.get_model(api, "CartItemOut")))
            }
        )

    @staticmethod
    def marshall_json(data_out):
        schema = CartSchema()
        jsonsend = schema.load(data_out)
        return jsonsend
