from marshmallow import Schema, fields, validates

from ..models.product_item import ProductItemSchema
from backend.errors.request_error import ValidationError


class ProductListSchema(Schema):
    item_list = fields.List(fields.Nested(ProductItemSchema, required=True), required=True)

    @validates("item_list")
    def validate_id_list(self, value):
        if not value:
            raise ValidationError("item_list cannot be an empty list.")
