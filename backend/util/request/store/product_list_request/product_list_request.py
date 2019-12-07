from flask import request
from flask_restplus import fields

from ..models.product_item import ProductItemRequest
from .product_list_schema import ProductListSchema


class ProductListRequest(object):
    @staticmethod
    def get_model(api, name):
        return api.model(
            name,
            {
                "item_list": fields.List(fields.Nested(ProductItemRequest.get_model(api, "ProductItemRequest"), required=True), required=True)
            }
        )

    @staticmethod
    def parse_json():
        jsonrecv = request.get_json()
        schema = ProductListSchema()
        in_data = schema.load(jsonrecv)
        return in_data
