from flask_restplus import Namespace, Resource
from flask_login import login_required

from backend.service import CartService
from backend.util.response.cart import CartResponse
from backend.util.response.error import ErrorResponse
from backend.controller import ErrorHandler


selectAllNS = Namespace("Cart", description="Cart related operations.")

RESPONSEMODEL = CartResponse.get_model(selectAllNS, "CartResponse")
ERRORMODEL = ErrorResponse.get_model(selectAllNS, "ErrorResponse")


@selectAllNS.route("", strict_slashes=False)
class SelectAllController(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__cartservice = CartService()

    @login_required
    @selectAllNS.doc(security=["login"])
    @selectAllNS.response(200, "Success", RESPONSEMODEL)
    @selectAllNS.response(204, "No Content", {})
    @selectAllNS.response(401, "Unauthorized", ERRORMODEL)
    @selectAllNS.response(500, "Unexpected Error", ERRORMODEL)
    def get(self):
        """Cart items information."""
        try:
            jsonsend = CartResponse.marshall_json({"item_list": self.__cartservice.to_list()})
            return jsonsend
        except Exception as error:
            return ErrorHandler(error).handle_error()
