from flask import request
from flask_restplus import fields

from .user_orders_schema import UserOrdersSchema
from ..models.datespan import DatespanRequest


class UserOrdersRequest(object):
    @staticmethod
    def get_model(api, name):
        return api.model(
            name,
            {
                "page": fields.Integer(description="Page requested.", default=1),
                "page_size": fields.Integer(description="Amount of results per page.", default=10),
                "datespan": fields.Nested(DatespanRequest.get_model(api, "DatespanRequest"), description="Search date interval.")
            }
        )

    @staticmethod
    def parse_json():
        jsonrecv = request.get_json()
        if jsonrecv is not None:
            schema = UserOrdersSchema()
            schema.load(jsonrecv)
            return jsonrecv
        else:
            return {}
