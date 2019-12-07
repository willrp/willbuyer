from flask_restplus import fields


class DatespanRequest(object):
    @staticmethod
    def get_model(api, name):
        return api.model(
            name,
            {
                "start": fields.Date(description="Span start", required=True, example="YYYY-MM-DD"),
                "end": fields.Date(description="Span end", required=True, example="YYYY-MM-DD"),
            }
        )
