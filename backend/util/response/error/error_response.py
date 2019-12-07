from flask_restplus import fields
from flask import json

from .error_schema import ErrorSchema


class ErrorResponse(object):
    @staticmethod
    def get_model(api, name):
        return api.model(
            name,
            {
                "error": fields.String(required=True)
            }
        )

    @staticmethod
    def parse_HTTPError(content):
        jsonrecv = json.loads(content)
        if "error" in jsonrecv:
            schema = ErrorSchema()
            jsonsend = schema.load(jsonrecv)
            error = jsonsend["error"]
            return error
        else:
            return {}
