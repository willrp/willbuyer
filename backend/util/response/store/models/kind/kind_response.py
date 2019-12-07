from flask_restplus import fields


class KindResponse(object):
    @staticmethod
    def get_model(api, name):
        return api.model(
            name,
            {
                "kind": fields.String,
                "amount": fields.Integer(example=10)
            }
        )
