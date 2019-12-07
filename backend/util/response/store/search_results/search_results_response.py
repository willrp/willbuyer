from flask_restplus import fields

from ..models.brand import BrandResponse
from ..models.kind import KindResponse
from ..models.price_range import PriceRangeResponse
from .search_results_schema import SearchResultsSchema


class SearchResultsResponse(object):
    @staticmethod
    def get_model(api, name):
        return api.model(
            name,
            {
                "total": fields.Integer,
                "pricerange": fields.Nested(PriceRangeResponse.get_model(api, "PriceRangeOut")),
                "brands": fields.List(fields.Nested(BrandResponse.get_model(api, "BrandOut"))),
                "kinds": fields.List(fields.Nested(KindResponse.get_model(api, "KindOut")))
            }
        )

    @staticmethod
    def marshall_json(data_out):
        schema = SearchResultsSchema()
        jsonsend = schema.load(data_out)
        return jsonsend
