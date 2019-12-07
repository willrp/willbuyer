import os
from flask import current_app as app
from flask_restplus import Namespace, Resource
from flask_login import login_required
from requests import get

from backend.util.response.store.product_results import ProductResultsResponse
from backend.util.response.error import ErrorResponse
from backend.controller import ErrorHandler


productNS = Namespace("Store", description="Store related operations.")

RESPONSEMODEL = ProductResultsResponse.get_model(productNS, "ProductResultsResponse")
ERRORMODEL = ErrorResponse.get_model(productNS, "ErrorResponse")


@productNS.route("/product/<string:productid>", strict_slashes=False)
class ProductController(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__url = app.config["WILLSTORES_WS"]
        self.__headers = {"Authorization": "Bearer %s" % os.getenv("ACCESS_TOKEN")}

    @login_required
    @productNS.doc(security=["login"])
    @productNS.param("productid", description="The desired product ID", _in="path", required=True)
    @productNS.response(200, "Success", RESPONSEMODEL)
    @productNS.response(401, "Unauthorized", ERRORMODEL)
    @productNS.response(404, "Not Found", {})
    @productNS.response(500, "Unexpected Error", ERRORMODEL)
    @productNS.response(504, "Error while accessing the gateway server", ERRORMODEL)
    def get(self, productid):
        """Product information."""
        try:
            req = get("%s/api/product/%s" % (self.__url, productid), headers=self.__headers)
            req.raise_for_status()

            jsonsend = ProductResultsResponse.marshall_json(req.json())
            return jsonsend
        except Exception as error:
            return ErrorHandler(error).handle_error()
