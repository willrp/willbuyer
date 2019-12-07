from flask_restplus import fields

from ..models.price import PriceResponse
from .product_results_schema import ProductResultsSchema


class ProductResultsResponse(object):
    @staticmethod
    def get_model(api, name):
        return api.model(
            name,
            {
                "id": fields.String,
                "name": fields.String,
                "kind": fields.String,
                "brand": fields.String,
                "details": fields.List(fields.String),
                "care": fields.String,
                "about": fields.String,
                "images": fields.List(fields.String),
                "gender": fields.String,
                "price": fields.Nested(PriceResponse.get_model(api, "PriceOut"))
            }
        )

    @staticmethod
    def marshall_json(data_out):
        schema = ProductResultsSchema()
        jsonsend = schema.load(data_out)
        return jsonsend
