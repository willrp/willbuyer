from flask_restplus import fields

from ..models.brand import BrandResponse
from ..models.kind import KindResponse
from ..models.price_range import PriceRangeResponse
from ..models.session import SessionResponse
from .session_results_schema import SessionResultsSchema


class SessionResultsResponse(object):
    @staticmethod
    def get_model(api, name):
        return api.model(
            name,
            {
                "total": fields.Integer,
                "pricerange": fields.Nested(PriceRangeResponse.get_model(api, "PriceRangeOut")),
                "brands": fields.List(fields.Nested(BrandResponse.get_model(api, "BrandOut"))),
                "kinds": fields.List(fields.Nested(KindResponse.get_model(api, "KindOut"))),
                "sessions": fields.List(fields.Nested(SessionResponse.get_model(api, "SessionOut")))
            }
        )

    @staticmethod
    def marshall_json(data_out):
        schema = SessionResultsSchema()
        jsonsend = schema.load(data_out)
        return jsonsend
