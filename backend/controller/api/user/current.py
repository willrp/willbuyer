from flask_restplus import Namespace, Resource
from flask_login import current_user, login_required

from backend.util.response.user import UserResponse
from backend.util.response.error import ErrorResponse
from backend.controller import ErrorHandler


currentNS = Namespace("User", description="User related operations.")

RESPONSEMODEL = UserResponse.get_model(currentNS, "UserResponse")
ERRORMODEL = ErrorResponse.get_model(currentNS, "ErrorResponse")


@currentNS.route("/current", strict_slashes=False)
class CurrentController(Resource):
    @login_required
    @currentNS.doc(security=["login"])
    @currentNS.marshal_with(RESPONSEMODEL, code=200, description="Success", mask=False)
    @currentNS.response(401, "Unauthorized", ERRORMODEL)
    @currentNS.response(500, "Unexpected Error", ERRORMODEL)
    def get(self):
        """Get current (logged in) user"""
        try:
            jsonsend = UserResponse.marshall_json(current_user.to_dict())
            return jsonsend
        except Exception as error:
            return ErrorHandler(error).handle_error()
