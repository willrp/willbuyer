from flask import request
from flask_restplus import fields

from ..models.price_range import PriceRangeRequest
from .search_products_schema import SearchProductsSchema


class SearchProductsRequest(object):
    @staticmethod
    def get_model(api, name):
        return api.model(
            name,
            {
                "pagesize": fields.Integer(example=20),
                "pricerange": fields.Nested(PriceRangeRequest.get_model(api, "PriceRangeIn"))
            }
        )

    @staticmethod
    def parse_json():
        jsonrecv = request.get_json()
        if jsonrecv is not None:
            schema = SearchProductsSchema()
            in_data = schema.load(jsonrecv)
            return in_data
        else:
            return {}
