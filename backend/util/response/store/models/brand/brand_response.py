from flask_restplus import fields


class BrandResponse(object):
    @staticmethod
    def get_model(api, name):
        return api.model(
            name,
            {
                "brand": fields.String,
                "amount": fields.Integer(example=10)
            }
        )
