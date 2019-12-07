import os
from flask import current_app as app
from flask_restplus import Namespace, Resource
from flask_login import login_required
from requests import get

from backend.service import CartService
from backend.util.response.error import ErrorResponse
from backend.controller import ErrorHandler
from backend.errors.request_error import ValidationError


updateNS = Namespace("Cart", description="Cart related operations.")

ERRORMODEL = ErrorResponse.get_model(updateNS, "ErrorResponse")


@updateNS.route("/update/<string:item_id>/<int:amount>", strict_slashes=False)
class UpdateController(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__cartservice = CartService()
        self.__url = app.config["WILLSTORES_WS"]
        self.__headers = {"Authorization": "Bearer %s" % os.getenv("ACCESS_TOKEN")}

    @login_required
    @updateNS.doc(security=["login"])
    @updateNS.param("item_id", description="Item ID", _in="path", required=True)
    @updateNS.param("amount", description="Amount", _in="path", required=True)
    @updateNS.response(200, description="Success", mask=False)
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
                req = get("%s/api/product/%s" % (self.__url, item_id), headers=self.__headers)

                if req.status_code == 404:
                    raise ValidationError("'%s' is an invalid item ID." % item_id)

                req.raise_for_status()

                self.__cartservice.update_item(item_id, amount)
                return {}, 200
        except Exception as error:
            return ErrorHandler(error).handle_error()
