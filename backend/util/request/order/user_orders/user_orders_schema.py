
from marshmallow import Schema, fields, validates

from backend.errors.request_error import ValidationError
from ..models.datespan import DatespanSchema


class UserOrdersSchema(Schema):
    page = fields.Integer()
    page_size = fields.Integer()
    datespan = fields.Nested(DatespanSchema)

    @validates("page")
    def validate_page(self, value, **kwargs):
        if value <= 0:
            raise ValidationError("'page' must be a natural positive number.")

    @validates("page_size")
    def validate_page_size(self, value, **kwargs):
        if value <= 0:
            raise ValidationError("'page_size' must be a natural positive number.")
        elif value > 100:
            raise ValidationError("'page_size' must be a natural positive number.")
