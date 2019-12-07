from marshmallow import Schema, fields

from ..models.brand import BrandSchema
from ..models.kind import KindSchema
from ..models.price_range import PriceRangeSchema


class SearchResultsSchema(Schema):
    total = fields.Integer(required=True)
    pricerange = fields.Nested(PriceRangeSchema, required=True)
    brands = fields.Nested(BrandSchema, required=True, many=True)
    kinds = fields.Nested(KindSchema, required=True, many=True)
