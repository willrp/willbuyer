from marshmallow import Schema, fields

from ..models.price_range import PriceRangeSchema


class SearchSchema(Schema):
    pricerange = fields.Nested(PriceRangeSchema)
