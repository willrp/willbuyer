from flask import redirect, url_for, current_app as app
from flask_restplus import Namespace, Resource
from flask_login import current_user, logout_user

from backend.util.response.error import ErrorResponse
from backend.controller import ErrorHandler


logoutNS = Namespace("User", description="User authentication with OAuth2.")

ERRORMODEL = ErrorResponse.get_model(logoutNS, "ErrorResponse")


@logoutNS.route("", strict_slashes=False)
class LogoutController(Resource):
    @logoutNS.response(302, "Logout and/or redirect to index")
    @logoutNS.response(500, "Unexpected Error", ERRORMODEL)
    def get(self):
        """User Logout"""
        try:
            if current_user.is_authenticated is False:
                return redirect(url_for("frontend.index"))
            else:
                provider = current_user.provider
                blueprint = app.blueprints[provider]
                if blueprint.token:
                    try:
                        blueprint.session.post(
                            "https://accounts.google.com/o/oauth2/revoke",
                            params={"token": blueprint.token["access_token"]},
                            headers={"Content-Type": "application/x-www-form-urlencoded"}
                        )
                    except Exception:
                        pass

                del blueprint.token
                logout_user()
                return redirect(url_for("frontend.index"))
        except Exception as error:
            return ErrorHandler(error).handle_error()
