import os
from flask import current_app as app
from flask_restplus import Namespace, Resource
from requests import post

from backend.service import CartService
from backend.util.response.cart import CartResponse
from backend.util.response.error import ErrorResponse
from backend.controller import ErrorHandler
from backend.errors.no_content_error import NoContentError


removeNS = Namespace("Cart", description="Cart related operations.")

RESPONSEMODEL = CartResponse.get_model(removeNS, "CartResponse")
ERRORMODEL = ErrorResponse.get_model(removeNS, "ErrorResponse")


@removeNS.route("/remove/<string:item_id>", strict_slashes=False)
class RemoveController(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__cartservice = CartService()
        self.__url = app.config["WILLSTORES_WS"]
        self.__headers = {"Authorization": "Bearer %s" % os.getenv("ACCESS_TOKEN")}

    @removeNS.param("item_id", description="Item ID", _in="path", required=True)
    @removeNS.response(200, "Success", RESPONSEMODEL)
    @removeNS.response(204, "No Content", {})
    @removeNS.response(400, "Bad Request", ERRORMODEL)
    @removeNS.response(401, "Unauthorized", ERRORMODEL)
    @removeNS.response(500, "Unexpected Error", ERRORMODEL)
    def post(self, item_id):
        """Item removal."""
        try:
            self.__cartservice.remove_item(item_id)
            item_list = self.__cartservice.to_list()

            if item_list == []:
                raise NoContentError()
            else:
                items_info = {"item_list": item_list}

                req = post("%s/api/product/list" % (self.__url), headers=self.__headers, json=items_info)
                req.raise_for_status()
                result = req.json()

                for item in item_list:
                    product = next(p for p in result["products"] if p["id"] == item["item_id"])
                    product["amount"] = item["amount"]

                jsonsend = CartResponse.marshall_json(dict(**result))
                return jsonsend
        except Exception as error:
            return ErrorHandler(error).handle_error()
