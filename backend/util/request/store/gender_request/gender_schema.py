from marshmallow import Schema, fields, validates

from backend.errors.request_error import ValidationError


class GenderSchema(Schema):
    amount = fields.Integer()

    @validates("amount")
    def validate_amount(self, value):
        if value <= 0:
            raise ValidationError("Invalid amount '%s', must be positive" % value)
