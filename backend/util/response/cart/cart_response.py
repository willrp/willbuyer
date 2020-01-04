from flask_restplus import fields

from .models.product import ProductResponse
from .models.price import PriceResponse
from .cart_schema import CartSchema


class CartResponse(object):
    @staticmethod
    def get_model(api, name):
        return api.model(
            name,
            {
                "products": fields.List(fields.Nested(ProductResponse.get_model(api, "ProductsCartOut"))),
                "total": fields.Nested(PriceResponse.get_model(api, "TotalCartOut"))
            }
        )

    @staticmethod
    def marshall_json(data_out):
        schema = CartSchema()
        jsonsend = schema.load(data_out)
        return jsonsend
