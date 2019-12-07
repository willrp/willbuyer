from marshmallow import Schema, fields, EXCLUDE

from ..models.price import PriceSchema


class ProductResultsSchema(Schema):
    id = fields.String(required=True)
    name = fields.String(required=True)
    kind = fields.String(required=True)
    brand = fields.String(required=True)
    details = fields.Raw(required=True, many=True)
    care = fields.String(required=True)
    about = fields.String(required=True)
    images = fields.Raw(required=True, many=True)
    gender = fields.String(required=True)
    price = fields.Nested(PriceSchema, required=True)

    class Meta:
        unknown = EXCLUDE
