from flask import request
from flask_restplus import fields

from .gender_schema import GenderSchema


class GenderRequest(object):
    @staticmethod
    def get_model(api, name):
        return api.model(
            name,
            {
                "amount": fields.Integer(required=True, description="Amount of discounts provided", example=10)
            }
        )

    @staticmethod
    def parse_json():
        jsonrecv = request.get_json()
        if jsonrecv is not None:
            schema = GenderSchema()
            in_data = schema.load(jsonrecv)
            return in_data
        else:
            return {}
