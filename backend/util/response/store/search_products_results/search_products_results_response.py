from flask_restplus import fields

from ..models.product import ProductResponse
from .search_products_results_schema import SearchProductsResultsSchema


class SearchProductsResultsResponse(object):
    @staticmethod
    def get_model(api, name):
        return api.model(
            name,
            {
                "products": fields.List(fields.Nested(ProductResponse.get_model(api, "ProductOut")))
            }
        )

    @staticmethod
    def marshall_json(data_out):
        schema = SearchProductsResultsSchema()
        jsonsend = schema.load(data_out)
        return jsonsend
