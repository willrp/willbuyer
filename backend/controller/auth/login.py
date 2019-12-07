import os
from flask import redirect, url_for, request, session
from flask_restplus import Namespace, Resource
from flask_dance.contrib.google import make_google_blueprint
from flask_dance.consumer import oauth_authorized
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from flask_login import current_user, login_user

from backend.service import UserService
from backend.model import OAuth
from backend.dao.postgres_db import DBSession
from backend.util.response.error import ErrorResponse
from backend.util.safe_url import is_safe_url
from backend.controller import ErrorHandler


bplogin = make_google_blueprint(
    login_url="google_login",
    client_id=os.getenv("OAUTH_CLIENT_ID"),
    client_secret=os.getenv("OAUTH_CLIENT_SECRET"),
    scope=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    offline=True,
    redirect_url="",
    storage=SQLAlchemyStorage(OAuth, DBSession(), user=current_user)
)


@oauth_authorized.connect_via(bplogin)
def user_logged_in(blueprint, token):
    if not token:
        return redirect(url_for("frontend.index", error="token"))
    else:
        response = blueprint.session.get("/oauth2/v1/userinfo")

        if not response.ok:
            return redirect(url_for("frontend.index", error="error"))
        else:
            try:
                user_service = UserService()

                user_info = response.json()
                user_id = user_info["id"]

                oauth = user_service.get_create_oauth(provider=blueprint.name, provider_user_id=user_id, token=token)

                if not oauth.user:
                    email = user_info["email"]
                    name = user_info["name"]
                    picture = user_info["picture"]
                    user_service.get_create_user(oauth=oauth, email=email, name=name, picture=picture)

                login_user(oauth.user)
                return False
            except Exception:
                return redirect(url_for("frontend.index", error="error"))


loginNS = Namespace("User", description="User authentication with OAuth2.")

ERRORMODEL = ErrorResponse.get_model(loginNS, "ErrorResponse")


@loginNS.route("", strict_slashes=False)
class LoginAuthController(Resource):
    @loginNS.response(302, "Redirect to login URL or index")
    @loginNS.response(500, "Unexpected Error", ERRORMODEL)
    def get(self):
        """User login"""
        try:
            if current_user.is_authenticated is False:
                next_url = request.args.get("next")
                if next_url is not None and is_safe_url(next_url):
                    session["next_url"] = next_url

                return redirect(url_for("google.login"))
            else:
                return redirect(url_for("frontend.index"))
        except Exception as error:
            return ErrorHandler(error).handle_error()
