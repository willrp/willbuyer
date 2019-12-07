import os
from flask import current_app as app
from flask_restplus import Namespace, Resource
from flask_login import login_required, current_user
from requests import post

from backend.util.request.order.user_orders import UserOrdersRequest
from backend.util.response.order.user_orders import UserOrdersResponse
from backend.util.response.error import ErrorResponse
from backend.controller import ErrorHandler
from backend.errors.no_content_error import NoContentError


selectFromUserNS = Namespace("Order", description="Order related operations.")


REQUESTMODEL = UserOrdersRequest.get_model(selectFromUserNS, "UserOrdersRequest")
RESPONSEMODEL = UserOrdersResponse.get_model(selectFromUserNS, "UserOrdersResponse")
ERRORMODEL = ErrorResponse.get_model(selectFromUserNS, "ErrorResponse")


@selectFromUserNS.route("/user", strict_slashes=False)
class SelectFromUserController(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__url = app.config["WILLORDERS_WS"]
        self.__headers = {"Authorization": "Bearer %s" % os.getenv("ACCESS_TOKEN")}

    @login_required
    @selectFromUserNS.doc(security=["login"])
    @selectFromUserNS.param("payload", description="Optional", _in="body", required=False)
    @selectFromUserNS.expect(REQUESTMODEL)
    @selectFromUserNS.response(200, "Success", RESPONSEMODEL)
    @selectFromUserNS.response(204, "No Content", {})
    @selectFromUserNS.response(400, "Bad Request", ERRORMODEL)
    @selectFromUserNS.response(401, "Unauthorized", ERRORMODEL)
    @selectFromUserNS.response(500, "Unexpected Error", ERRORMODEL)
    @selectFromUserNS.response(502, "Error while accessing the gateway server", ERRORMODEL)
    @selectFromUserNS.response(504, "No response from gateway server", ERRORMODEL)
    def post(self):
        """Orders for the logged in user."""
        try:
            in_data = UserOrdersRequest.parse_json()
            user_slug = current_user.uuid_slug

            req = post("%s/api/order/user/%s" % (self.__url, user_slug), headers=self.__headers, json=in_data)
            req.raise_for_status()

            if req.status_code == 204:
                raise NoContentError()
            else:
                jsonsend = UserOrdersResponse.marshall_json(req.json())
                return jsonsend
        except Exception as error:
            return ErrorHandler(error).handle_error()
