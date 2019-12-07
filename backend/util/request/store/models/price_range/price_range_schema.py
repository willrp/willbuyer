from marshmallow import Schema, fields, validates_schema

from backend.errors.request_error import ValidationError


class PriceRangeSchema(Schema):
    min = fields.Float(required=True)
    max = fields.Float(required=True)

    @validates_schema(skip_on_field_errors=True)
    def validate_prices(self, data, **kwargs):
        valmin = data["min"]
        valmax = data["max"]
        if valmin <= 0.0:
            raise ValidationError("Invalid min '%s', must be positive" % valmin)
        elif valmax <= 0.0:
            raise ValidationError("Invalid max '%s', must be positive" % valmax)
        elif valmax < valmin:
            raise ValidationError("Max '%s' cannot be lower than min '%s'" % (valmax, valmin))
