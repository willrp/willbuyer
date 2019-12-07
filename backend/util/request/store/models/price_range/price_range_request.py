from flask_restplus import fields


class PriceRangeRequest(object):
    @staticmethod
    def get_model(api, name):
        return api.model(
            name,
            {
                "min": fields.Float(required=True, example=10.0),
                "max": fields.Float(required=True, example=20.0)
            }
        )
