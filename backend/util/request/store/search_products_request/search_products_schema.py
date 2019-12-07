from marshmallow import Schema, fields, validates

from ..models.price_range import PriceRangeSchema
from backend.errors.request_error import ValidationError


class SearchProductsSchema(Schema):
    pagesize = fields.Integer()
    pricerange = fields.Nested(PriceRangeSchema)

    @validates("pagesize")
    def validate_pagesize(self, value):
        if value <= 0:
            raise ValidationError("Invalid pagesize '%s', must be positive" % value)
