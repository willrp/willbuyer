import os
from flask_restplus import Namespace, Resource
from flask import current_app as app
from flask_login import login_required
from requests import post

from backend.util.request.store.search_request import SearchRequest
from backend.util.response.store.search_results import SearchResultsResponse
from backend.util.response.error import ErrorResponse
from backend.controller import ErrorHandler
from backend.errors.no_content_error import NoContentError
from backend.errors.request_error import ValidationError


findNS = Namespace("Store", description="Store related operations.")

REQUESTMODEL = SearchRequest.get_model(findNS, "SearchRequest")
RESPONSEMODEL = SearchResultsResponse.get_model(findNS, "SearchResultsResponse")
ERRORMODEL = ErrorResponse.get_model(findNS, "ErrorResponse")


@findNS.route("/find/<string:ftype>/<string:arg>/", strict_slashes=False)
class FinderController(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__url = app.config["WILLSTORES_WS"]
        self.__headers = {"Authorization": "Bearer %s" % os.getenv("ACCESS_TOKEN")}
        self.__finder_types = ["search", "brand", "kind"]

    @login_required
    @findNS.doc(security=["login"])
    @findNS.param("ftype", description="The product finder type: 'search', 'kind' or 'brand'", _in="path", required=True)
    @findNS.param("arg", description="The product finder argument: query, product kind or brand", _in="path", required=True)
    @findNS.param("payload", description="Optional", _in="body", required=False)
    @findNS.expect(REQUESTMODEL)
    @findNS.response(200, "Success", RESPONSEMODEL)
    @findNS.response(204, "No Content", {})
    @findNS.response(400, "Bad Request", ERRORMODEL)
    @findNS.response(401, "Unauthorized", ERRORMODEL)
    @findNS.response(500, "Unexpected Error", ERRORMODEL)
    @findNS.response(502, "Error while accessing the gateway server", ERRORMODEL)
    @findNS.response(504, "No response from the gateway server", ERRORMODEL)
    def post(self, ftype, arg):
        """Finder information by 'search query', 'kind' or 'brand'"""
        try:
            if ftype not in self.__finder_types:
                raise ValidationError("'%s' is an invalid URL finder type. Valid: 'search', 'brand' and 'kind'")
            else:
                in_data = SearchRequest.parse_json()
                req = post("%s/api/%s/%s" % (self.__url, ftype, arg), headers=self.__headers, json=in_data)
                req.raise_for_status()

                if req.status_code == 204:
                    raise NoContentError()
                else:
                    jsonsend = SearchResultsResponse.marshall_json(req.json())
                    return jsonsend
        except Exception as error:
            return ErrorHandler(error).handle_error()
