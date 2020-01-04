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


findProductsNS = Namespace("Store", description="Store related operations.")

REQUESTMODEL = SearchProductsRequest.get_model(findProductsNS, "SearchProductsRequest")
RESPONSEMODEL = SearchProductsResultsResponse.get_model(findProductsNS, "SearchProductsResultsResponse")
ERRORMODEL = ErrorResponse.get_model(findProductsNS, "ErrorResponse")


@findProductsNS.route("/find/<string:ftype>/<string:arg>/<int:page>/", strict_slashes=False)
class FinderProductsController(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__url = app.config["WILLSTORES_WS"]
        self.__headers = {"Authorization": "Bearer %s" % os.getenv("ACCESS_TOKEN")}
        self.__finder_types = ["search", "brand", "kind"]

    @findProductsNS.param("ftype", description="The product finder type: 'search', 'kind' or 'brand'", _in="path", required=True)
    @findProductsNS.param("arg", description="The product finder argument: query, product kind or brand", _in="path", required=True)
    @findProductsNS.param("page", description="The finder page.", _in="path", required=True)
    @findProductsNS.param("payload", description="Optional", _in="body", required=False)
    @findProductsNS.expect(REQUESTMODEL)
    @findProductsNS.response(200, "Success", RESPONSEMODEL)
    @findProductsNS.response(204, "No content", {})
    @findProductsNS.response(400, "Bad Request", ERRORMODEL)
    @findProductsNS.response(500, "Unexpected Error", ERRORMODEL)
    @findProductsNS.response(502, "Error while accessing the gateway server", ERRORMODEL)
    @findProductsNS.response(504, "No response from the gateway server", ERRORMODEL)
    def post(self, ftype, arg, page):
        """Finder products paginated by 'search query', 'kind' or 'brand'"""
        try:
            if ftype not in self.__finder_types:
                raise ValidationError("'%s' is an invalid URL finder type. Valid: 'search', 'brand' and 'kind'" % ftype)
            if page <= 0:
                raise ValidationError("'%s' is an invalid URL page value. It must be a positive natural number" % page)
            else:
                in_data = SearchProductsRequest.parse_json()
                req = post("%s/api/%s/%s/%s" % (self.__url, ftype, arg, page), headers=self.__headers, json=in_data)
                req.raise_for_status()

                if req.status_code == 204:
                    raise NoContentError()
                else:
                    jsonsend = SearchProductsResultsResponse.marshall_json(req.json())
                    return jsonsend
        except Exception as error:
            return ErrorHandler(error).handle_error()
