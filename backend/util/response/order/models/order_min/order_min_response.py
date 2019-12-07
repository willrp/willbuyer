from flask_restplus import fields

from ..price import PriceResponse


class OrderMinResponse(object):
    @staticmethod
    def get_model(api, name):
        return api.model(
            name,
            {
                "slug": fields.String(required=True),
                "user_slug": fields.String(required=True),
                "product_types": fields.Integer(required=True),
                "items_amount": fields.Integer(required=True),
                "total": fields.Nested(PriceResponse.get_model(api, "PriceOut"), required=True),
                "updated_at": fields.DateTime(required=True),
            }
        )
