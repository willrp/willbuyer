from flask_restplus import fields


class SessionResponse(object):
    @staticmethod
    def get_model(api, name):
        return api.model(
            name,
            {
                "id": fields.String,
                "name": fields.String,
                "gender": fields.String,
                "image": fields.String,
                "total": fields.Integer(example=100)
            }
        )
