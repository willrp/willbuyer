from flask_restplus import fields


class ProductItemRequest(object):
    @staticmethod
    def get_model(api, name):
        return api.model(
            name,
            {
                "item_id": fields.String(required=True),
                "amount": fields.Integer(required=True, example=1),
            }
        )
