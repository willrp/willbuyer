from flask_restplus import fields


class ItemResponse(object):
    @staticmethod
    def get_model(api, name):
        return api.model(
            name,
            {
                "item_id": fields.String(description="User e-mail.", required=True),
                "amount": fields.Integer(description="Item amount", required=True)
            }
        )
