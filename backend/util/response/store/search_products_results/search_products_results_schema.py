from marshmallow import Schema, fields

from ..models.product import ProductSchema


class SearchProductsResultsSchema(Schema):
    products = fields.Nested(ProductSchema, required=True, many=True)
