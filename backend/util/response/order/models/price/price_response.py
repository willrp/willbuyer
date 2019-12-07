from flask_restplus import fields


class PriceResponse(object):
    @staticmethod
    def get_model(api, name):
        return api.model(
            name,
            {
                "outlet": fields.Float(example=10.55),
                "retail": fields.Float(example=20.9),
                "symbol": fields.String(example="£")
            }
        )
