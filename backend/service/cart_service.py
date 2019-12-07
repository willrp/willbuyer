from flask import session

from ..errors.no_content_error import NoContentError
from ..errors.request_error import ValidationError


class CartService(object):
    def update_item(self, item_id: str, amount: int) -> bool:
        if "cart" not in session:
            session["cart"] = dict()

        session["cart"].update({item_id: amount})
        return True

    def remove_item(self, item_id: str) -> bool:
        try:
            session["cart"].pop(item_id)
            return True
        except KeyError:
            raise ValidationError("Item %s does not exist on cart" % item_id)

    def empty(self) -> bool:
        session["cart"] = dict()
        return True

    def to_dict(self) -> dict:
        try:
            return session["cart"]
        except KeyError:
            return {}

    def to_list(self) -> list:
        try:
            if not session["cart"]:
                raise NoContentError()
            else:
                return [{"item_id": key, "amount": value} for key, value in session["cart"].items()]
        except KeyError:
            raise NoContentError()
