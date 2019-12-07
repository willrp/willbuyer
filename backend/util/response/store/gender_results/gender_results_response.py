from flask_restplus import fields

from ..models.brand import BrandResponse
from ..models.discount import DiscountResponse
from ..models.kind import KindResponse
from ..models.session import SessionResponse
from .gender_results_schema import GenderResultsSchema


class GenderResultsResponse(object):
    @staticmethod
    def get_model(api, name):
        return api.model(
            name,
            {
                "discounts": fields.List(fields.Nested(DiscountResponse.get_model(api, "DiscountOut"))),
                "sessions": fields.List(fields.Nested(SessionResponse.get_model(api, "SessionOut"))),
                "brands": fields.List(fields.Nested(BrandResponse.get_model(api, "BrandOut"))),
                "kinds": fields.List(fields.Nested(KindResponse.get_model(api, "KindOut")))
            }
        )

    @staticmethod
    def marshall_json(data_out):
        schema = GenderResultsSchema()
        jsonsend = schema.load(data_out)
        return jsonsend
