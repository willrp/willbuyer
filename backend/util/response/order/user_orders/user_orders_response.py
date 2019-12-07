from flask_restplus import fields

from ..models.order_min import OrderMinResponse
from .user_orders_schema import UserOrdersSchema


class UserOrdersResponse(object):
    @staticmethod
    def get_model(api, name):
        return api.model(
            name,
            {
                "orders": fields.List(fields.Nested(OrderMinResponse.get_model(api, "OrderMinResponse"), required=True), required=True),
                "total": fields.Integer(description="Amount of results", required=True),
                "pages": fields.Integer(description="Amount of pages", required=True)
            }
        )

    @staticmethod
    def marshall_json(dict_out):
        data_out = dict_out
        schema = UserOrdersSchema()
        jsonsend = schema.load(data_out)
        return jsonsend
