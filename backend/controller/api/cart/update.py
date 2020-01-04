import os
from flask import current_app as app
from flask_restplus import Namespace, Resource
from requests import get, post

from backend.service import CartService
from backend.util.response.cart import CartResponse
from backend.util.response.error import ErrorResponse
from backend.controller import ErrorHandler
from backend.errors.request_error import ValidationError


updateNS = Namespace("Cart", description="Cart related operations.")

RESPONSEMODEL = CartResponse.get_model(updateNS, "CartResponse")
ERRORMODEL = ErrorResponse.get_model(updateNS, "ErrorResponse")


@updateNS.route("/update/<string:item_id>/<int:amount>", strict_slashes=False)
class UpdateController(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__cartservice = CartService()
        self.__url = app.config["WILLSTORES_WS"]
        self.__headers = {"Authorization": "Bearer %s" % os.getenv("ACCESS_TOKEN")}

    @updateNS.param("item_id", description="Item ID", _in="path", required=True)
    @updateNS.param("amount", description="Amount", _in="path", required=True)
    @updateNS.response(200, "Success", RESPONSEMODEL)
    @updateNS.response(400, "Bad Request", ERRORMODEL)
    @updateNS.response(401, "Unauthorized", ERRORMODEL)
    @updateNS.response(500, "Unexpected Error", ERRORMODEL)
    @updateNS.response(502, "Error while accessing the gateway server", ERRORMODEL)
    @updateNS.response(504, "No response from gateway server", ERRORMODEL)
    def post(self, item_id, amount):
        """Item add or update."""
        try:
            if amount <= 0:
                raise ValidationError("'%s' is an invalid item amount. It must be a positive natural number" % amount)
            else:
                item_dict = self.__cartservice.to_dict()
                item_dict.update({item_id: amount})
                item_list = [{"item_id": key, "amount": value} for key, value in item_dict.items()]
                items_info = {"item_list": item_list}

                req = post("%s/api/product/list" % (self.__url), headers=self.__headers, json=items_info)
                req.raise_for_status()
                result = req.json()

                self.__cartservice.update_item(item_id, amount)

                for item in item_list:
                    product = next(p for p in result["products"] if p["id"] == item["item_id"])
                    product["amount"] = item["amount"]

                jsonsend = CartResponse.marshall_json(dict(**result))
                return jsonsend
        except Exception as error:
            return ErrorHandler(error).handle_error()
