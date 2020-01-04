import os
from flask import current_app as app
from flask_restplus import Namespace, Resource
from flask_login import login_required, current_user
from requests import get

from backend.util.response.order.order import OrderResponse
from backend.util.response.error import ErrorResponse
from backend.controller import ErrorHandler


selectBySlugNS = Namespace("Order", description="Order related operations.")

RESPONSEMODEL = OrderResponse.get_model(selectBySlugNS, "OrderResponse")
ERRORMODEL = ErrorResponse.get_model(selectBySlugNS, "ErrorResponse")


@selectBySlugNS.route("/<string:slug>", strict_slashes=False)
class SelectBySlugController(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__url = app.config["WILLORDERS_WS"]
        self.__headers = {"Authorization": "Bearer %s" % os.getenv("ACCESS_TOKEN")}

    @login_required
    @selectBySlugNS.doc(security=["login"])
    @selectBySlugNS.param("slug", description="Order slug", _in="path", required=True)
    @selectBySlugNS.response(200, "Success", RESPONSEMODEL)
    @selectBySlugNS.response(400, "Bad Request", ERRORMODEL)
    @selectBySlugNS.response(401, "Unauthorized", ERRORMODEL)
    @selectBySlugNS.response(404, "Not Found", ERRORMODEL)
    @selectBySlugNS.response(500, "Unexpected Error", ERRORMODEL)
    @selectBySlugNS.response(502, "Error while accessing the gateway server", ERRORMODEL)
    @selectBySlugNS.response(504, "No response from gateway server", ERRORMODEL)
    def get(self, slug):
        """Order information."""
        try:
            user_slug = current_user.uuid_slug

            req = get("%s/api/order/%s/%s" % (self.__url, user_slug, slug), headers=self.__headers)
            req.raise_for_status()

            jsonsend = OrderResponse.marshall_json(req.json())
            return jsonsend
        except Exception as error:
            return ErrorHandler(error).handle_error()
