from flask_restplus import fields

from ..models.price import PriceResponse
from ..models.product import ProductResponse
from .order_schema import OrderSchema


class OrderResponse(object):
    @staticmethod
    def get_model(api, name):
        return api.model(
            name,
            {
                "slug": fields.String(required=True),
                "user_slug": fields.String(required=True),
                "product_types": fields.Integer(required=True),
                "items_amount": fields.Integer(required=True),
                "total": fields.Nested(PriceResponse.get_model(api, "PriceOut"), required=True),
                "products": fields.List(fields.Nested(ProductResponse.get_model(api, "ProductOrderOut")), required=True),
                "updated_at": fields.DateTime(required=True),
            }
        )

    @staticmethod
    def marshall_json(dict_out):
        data_out = dict_out
        schema = OrderSchema()
        jsonsend = schema.load(data_out)
        return jsonsend
