import os
from flask_restplus import Namespace, Resource
from flask import current_app as app
from requests import post

from backend.util.request.store.search_products_request import SearchProductsRequest
from backend.util.response.store.search_products_results import SearchProductsResultsResponse
from backend.util.response.error import ErrorResponse
from backend.controller import ErrorHandler
from backend.errors.no_content_error import NoContentError
from backend.errors.request_error import ValidationError


sessionProductsNS = Namespace("Store", description="Store related operations.")

REQUESTMODEL = SearchProductsRequest.get_model(sessionProductsNS, "SearchProductsRequest")
RESPONSEMODEL = SearchProductsResultsResponse.get_model(sessionProductsNS, "SearchProductsResultsResponse")
ERRORMODEL = ErrorResponse.get_model(sessionProductsNS, "ErrorResponse")


@sessionProductsNS.route("/session/<string:sessionid>/<int:page>", strict_slashes=False)
class SessionProductsController(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__url = app.config["WILLSTORES_WS"]
        self.__headers = {"Authorization": "Bearer %s" % os.getenv("ACCESS_TOKEN")}

    @sessionProductsNS.param("sessionid", description="The desired session ID", _in="path", required=True)
    @sessionProductsNS.param("page", description="The search page.", _in="path", required=True)
    @sessionProductsNS.param("payload", description="Optional", _in="body", required=False)
    @sessionProductsNS.expect(REQUESTMODEL)
    @sessionProductsNS.response(200, "Success", RESPONSEMODEL)
    @sessionProductsNS.response(204, "No content", {})
    @sessionProductsNS.response(400, "Bad Request", ERRORMODEL)
    @sessionProductsNS.response(500, "Unexpected Error", ERRORMODEL)
    @sessionProductsNS.response(502, "Error while accessing the gateway server", ERRORMODEL)
    @sessionProductsNS.response(504, "No response from the gateway server", ERRORMODEL)
    def post(self, sessionid, page):
        """Session products paginated"""
        try:
            if page <= 0:
                raise ValidationError("'%s' is an invalid URL page value. It must be a positive natural number" % page)
            else:
                in_data = SearchProductsRequest.parse_json()
                req = post("%s/api/session/%s/%s" % (self.__url, sessionid, page), headers=self.__headers, json=in_data)
                req.raise_for_status()

                if req.status_code == 204:
                    raise NoContentError()

                jsonsend = SearchProductsResultsResponse.marshall_json(req.json())
                return jsonsend
        except Exception as error:
            return ErrorHandler(error).handle_error()
