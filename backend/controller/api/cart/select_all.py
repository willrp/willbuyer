import os
from flask import current_app as app
from flask_restplus import Namespace, Resource
from requests import post

from backend.service import CartService
from backend.util.response.cart import CartResponse
from backend.util.response.error import ErrorResponse
from backend.controller import ErrorHandler
from backend.errors.no_content_error import NoContentError


selectAllNS = Namespace("Cart", description="Cart related operations.")

RESPONSEMODEL = CartResponse.get_model(selectAllNS, "CartResponse")
ERRORMODEL = ErrorResponse.get_model(selectAllNS, "ErrorResponse")


@selectAllNS.route("", strict_slashes=False)
class SelectAllController(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__cartservice = CartService()
        self.__url = app.config["WILLSTORES_WS"]
        self.__headers = {"Authorization": "Bearer %s" % os.getenv("ACCESS_TOKEN")}

    @selectAllNS.response(200, "Success", RESPONSEMODEL)
    @selectAllNS.response(204, "No Content", {})
    @selectAllNS.response(401, "Unauthorized", ERRORMODEL)
    @selectAllNS.response(500, "Unexpected Error", ERRORMODEL)
    @selectAllNS.response(502, "Error while accessing the gateway server", ERRORMODEL)
    @selectAllNS.response(504, "No response from gateway server", ERRORMODEL)
    def get(self):
        """Cart items information."""
        try:
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
