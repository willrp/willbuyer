from flask_restplus import fields

from ..price import PriceResponse


class DiscountResponse(object):
    @staticmethod
    def get_model(api, name):
        return api.model(
            name,
            {
                "id": fields.String,
                "name": fields.String,
                "image": fields.String,
                "price": fields.Nested(PriceResponse.get_model(api, "PriceOut")),
                "discount": fields.Float(example=80.5)
            }
        )
