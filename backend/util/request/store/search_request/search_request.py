from flask import request
from flask_restplus import fields

from ..models.price_range import PriceRangeRequest
from .search_schema import SearchSchema


class SearchRequest(object):
    @staticmethod
    def get_model(api, name):
        return api.model(
            name,
            {
                "pricerange": fields.Nested(PriceRangeRequest.get_model(api, "PriceRangeIn"))
            }
        )

    @staticmethod
    def parse_json():
        jsonrecv = request.get_json()
        if jsonrecv is not None:
            schema = SearchSchema()
            in_data = schema.load(jsonrecv)
            return in_data
        else:
            return {}
