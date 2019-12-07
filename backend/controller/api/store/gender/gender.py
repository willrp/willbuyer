import os
from flask_restplus import Namespace, Resource
from flask import current_app as app
from flask_login import login_required
from requests import post

from backend.util.request.store.gender_request import GenderRequest
from backend.util.response.store.gender_results import GenderResultsResponse
from backend.util.response.error import ErrorResponse
from backend.controller import ErrorHandler
from backend.errors.no_content_error import NoContentError


genderNS = Namespace("Store", description="Store related operations.")

REQUESTMODEL = GenderRequest.get_model(genderNS, "GenderRequest")
RESPONSEMODEL = GenderResultsResponse.get_model(genderNS, "GenderResultsResponse")
ERRORMODEL = ErrorResponse.get_model(genderNS, "ErrorResponse")


@genderNS.route("/gender/<string:gender>", strict_slashes=False)
class GenderController(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__url = app.config["WILLSTORES_WS"]
        self.__headers = {"Authorization": "Bearer %s" % os.getenv("ACCESS_TOKEN")}

    @login_required
    @genderNS.doc(security=["login"])
    @genderNS.param("gender", description="The desired gender, 'Men' or 'Women'", _in="path", required=True)
    @genderNS.param("payload", description="Optional", _in="body", required=False)
    @genderNS.expect(REQUESTMODEL)
    @genderNS.response(200, "Success", RESPONSEMODEL)
    @genderNS.response(204, "No Content", {})
    @genderNS.response(400, "Bad Request", ERRORMODEL)
    @genderNS.response(401, "Unauthorized", ERRORMODEL)
    @genderNS.response(500, "Unexpected Error", ERRORMODEL)
    @genderNS.response(502, "Error while accessing the gateway server", ERRORMODEL)
    @genderNS.response(504, "No response from the gateway server", ERRORMODEL)
    def post(self, gender="Men"):
        """Gender information."""
        try:
            in_data = GenderRequest.parse_json()
            req = post("%s/api/gender/%s" % (self.__url, gender), headers=self.__headers, json=in_data)
            req.raise_for_status()

            if req.status_code == 204:
                raise NoContentError()

            jsonsend = GenderResultsResponse.marshall_json(req.json())
            return jsonsend
        except Exception as error:
            return ErrorHandler(error).handle_error()
