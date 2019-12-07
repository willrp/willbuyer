import os
from flask_restplus import Namespace, Resource
from flask import current_app as app
from flask_login import login_required
from requests import post

from backend.util.request.store.search_request import SearchRequest
from backend.util.response.store.session_results import SessionResultsResponse
from backend.util.response.error import ErrorResponse
from backend.controller import ErrorHandler
from backend.errors.no_content_error import NoContentError


sessionNS = Namespace("Store", description="Store related operations.")

REQUESTMODEL = SearchRequest.get_model(sessionNS, "SearchRequest")
RESPONSEMODEL = SessionResultsResponse.get_model(sessionNS, "SessionResultsResponse")
ERRORMODEL = ErrorResponse.get_model(sessionNS, "ErrorResponse")


@sessionNS.route("/session/<string:sessionid>", strict_slashes=False)
class SessionController(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__url = app.config["WILLSTORES_WS"]
        self.__headers = {"Authorization": "Bearer %s" % os.getenv("ACCESS_TOKEN")}

    @login_required
    @sessionNS.doc(security=["login"])
    @sessionNS.param("sessionid", description="The desired session ID", _in="path", required=True)
    @sessionNS.param("payload", description="Optional", _in="body", required=False)
    @sessionNS.expect(REQUESTMODEL)
    @sessionNS.response(200, "Success", RESPONSEMODEL)
    @sessionNS.response(204, "No products found", ERRORMODEL)
    @sessionNS.response(400, "Bad Request", ERRORMODEL)
    @sessionNS.response(401, "Unauthorized", ERRORMODEL)
    @sessionNS.response(404, "Not Found", {})
    @sessionNS.response(500, "Unexpected Error", ERRORMODEL)
    @sessionNS.response(502, "Error while accessing the gateway server", ERRORMODEL)
    @sessionNS.response(504, "No response from the gateway server", ERRORMODEL)
    def post(self, sessionid):
        """Session information."""
        try:
            in_data = SearchRequest.parse_json()
            req = post("%s/api/session/%s" % (self.__url, sessionid), headers=self.__headers, json=in_data)
            req.raise_for_status()

            if req.status_code == 204:
                raise NoContentError()

            jsonsend = SessionResultsResponse.marshall_json(req.json())
            return jsonsend
        except Exception as error:
            return ErrorHandler(error).handle_error()
