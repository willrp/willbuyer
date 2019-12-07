import os
from flask import current_app as app
from flask_restplus import Namespace, Resource
from flask_login import login_required, current_user
from requests import put

from backend.service import CartService
from backend.util.response.error import ErrorResponse
from backend.controller import ErrorHandler
from backend.errors.no_content_error import NoContentError
from backend.errors.request_error import ValidationError


orderNS = Namespace("Cart", description="Cart related operations.")

ERRORMODEL = ErrorResponse.get_model(orderNS, "ErrorResponse")


@orderNS.route("/order", strict_slashes=False)
class OrderController(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__cartservice = CartService()
        self.__url = app.config["WILLORDERS_WS"]
        self.__headers = {"Authorization": "Bearer %s" % os.getenv("ACCESS_TOKEN")}

    @login_required
    @orderNS.doc(security=["login"])
    @orderNS.response(201, description="Created", mask=False)
    @orderNS.response(400, "Bad Request", ERRORMODEL)
    @orderNS.response(401, "Unauthorized", ERRORMODEL)
    @orderNS.response(500, "Unexpected Error", ERRORMODEL)
    @orderNS.response(502, "Error while accessing the gateway server", ERRORMODEL)
    @orderNS.response(504, "No response from gateway server", ERRORMODEL)
    def put(self):
        """Make an order based on the cart items."""
        try:
            try:
                item_list = self.__cartservice.to_list()
            except NoContentError:
                raise ValidationError("Cart is empty")

            json_order = {
                "user_slug": current_user.uuid_slug,
                "item_list": item_list
            }

            req = put("%s/api/order/insert" % (self.__url), headers=self.__headers, json=json_order)
            req.raise_for_status()

            self.__cartservice.empty()

            return {}, 201
        except Exception as error:
            return ErrorHandler(error).handle_error()
