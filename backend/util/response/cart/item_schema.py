from marshmallow import Schema, fields


class ItemSchema(Schema):
    item_id = fields.String(required=True)
    amount = fields.Integer(required=True)
