from marshmallow import Schema, fields

from ..models.brand import BrandSchema
from ..models.discount import DiscountSchema
from ..models.kind import KindSchema
from ..models.session import SessionSchema


class GenderResultsSchema(Schema):
    discounts = fields.Nested(DiscountSchema, required=True, many=True)
    sessions = fields.Nested(SessionSchema, required=True, many=True)
    brands = fields.Nested(BrandSchema, required=True, many=True)
    kinds = fields.Nested(KindSchema, required=True, many=True)
