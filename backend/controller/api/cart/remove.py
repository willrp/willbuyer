from flask_restplus import Namespace, Resource
from flask_login import login_required

from backend.service import CartService
from backend.util.response.error import ErrorResponse
from backend.controller import ErrorHandler


removeNS = Namespace("Cart", description="Cart related operations.")

ERRORMODEL = ErrorResponse.get_model(removeNS, "ErrorResponse")


@removeNS.route("/remove/<string:item_id>", strict_slashes=False)
class RemoveController(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__cartservice = CartService()

    @login_required
    @removeNS.doc(security=["login"])
    @removeNS.param("item_id", description="Item ID", _in="path", required=True)
    @removeNS.response(200, description="Success", mask=False)
    @removeNS.response(400, "Bad Request", ERRORMODEL)
    @removeNS.response(401, "Unauthorized", ERRORMODEL)
    @removeNS.response(500, "Unexpected Error", ERRORMODEL)
    def post(self, item_id):
        """Item removal."""
        try:
            self.__cartservice.remove_item(item_id)
            return {}, 200
        except Exception as error:
            return ErrorHandler(error).handle_error()
