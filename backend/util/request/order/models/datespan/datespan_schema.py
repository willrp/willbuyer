from marshmallow import Schema, fields, validates_schema
from backend.errors.request_error import ValidationError


class DatespanSchema(Schema):
    start = fields.Date(format="%Y-%m-%d", required=True)
    end = fields.Date(format="%Y-%m-%d", required=True)

    @validates_schema
    def validate_datespan(self, data, **kwargs):
        if data["start"] > data["end"]:
            raise ValidationError("'start' has to be a date prior to 'end'")
