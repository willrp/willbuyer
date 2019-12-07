from flask_restplus import fields

from .user_schema import UserSchema


class UserResponse(object):
    @staticmethod
    def get_model(api, name):
        return api.model(
            name,
            {
                "email": fields.String(description="User e-mail.", required=True),
                "name": fields.String(description="User name.", required=True),
                "picture": fields.String(description="User picture URL.", required=True)
            }
        )

    @staticmethod
    def marshall_json(dict_out):
        data_out = dict_out
        schema = UserSchema()
        jsonsend = schema.load(data_out)
        return jsonsend
