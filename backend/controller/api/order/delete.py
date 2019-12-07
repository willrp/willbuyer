import os
from flask import current_app as app
from flask_restplus import Namespace, Resource
from flask_login import login_required
from requests import delete

from backend.util.response.error import ErrorResponse
from backend.controller import ErrorHandler


deleteNS = Namespace("Order", description="Order related operations.")

ERRORMODEL = ErrorResponse.get_model(deleteNS, "ErrorResponse")


@deleteNS.route("/delete/<string:slug>", strict_slashes=False)
class DeleteController(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__url = app.config["WILLORDERS_WS"]
        self.__headers = {"Authorization": "Bearer %s" % os.getenv("ACCESS_TOKEN")}

    @login_required
    @deleteNS.doc(security=["login"])
    @deleteNS.param("slug", description="Order slug", _in="path", required=True)
    @deleteNS.response(200, description="Deleted with success", mask=False)
    @deleteNS.response(400, "Bad Request", ERRORMODEL)
    @deleteNS.response(401, "Unauthorized", ERRORMODEL)
    @deleteNS.response(404, "Not Found", ERRORMODEL)
    @deleteNS.response(500, "Unexpected Error", ERRORMODEL)
    @deleteNS.response(502, "Error while accessing the gateway server", ERRORMODEL)
    @deleteNS.response(504, "No response from gateway server", ERRORMODEL)
    def delete(self, slug):
        """Order delete."""
        try:
            req = delete("%s/api/order/delete/%s" % (self.__url, slug), headers=self.__headers)
            req.raise_for_status()

            return {}, req.status_code
        except Exception as error:
            return ErrorHandler(error).handle_error()
