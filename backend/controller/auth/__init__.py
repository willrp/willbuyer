import os
from flask import Blueprint, redirect, url_for
from flask_restplus import Api, abort
from flask_login import LoginManager, user_logged_in
from oauthlib.oauth2.rfc6749.errors import InvalidGrantError, MissingCodeError, MismatchingStateError

from .login import bplogin, loginNS
from .logout import logoutNS
from backend.model import User
from backend.dao.postgres_db import DBSession


login_manager = LoginManager()

bpauth = Blueprint("auth", __name__)

auth = Api(bpauth,
    title="WillBuyer Authentication",
    description="WillBuyer API - Authentication",
    version="0.0.1",
    doc=("/" if os.getenv("FLASK_ENV") != "production" else False),
)

auth.namespaces.clear()
auth.add_namespace(loginNS, path="/login")
auth.add_namespace(logoutNS, path="/logout")


@user_logged_in.connect_via(bplogin)
def refresh_user_logged_in():
    login_manager.refresh_view = "google.login"


@login_manager.user_loader
def load_user(user_id):
    db_session = DBSession()
    return db_session.query(User).filter_by(id=user_id).one_or_none()


@login_manager.unauthorized_handler
def unauthorized():
    error = "Unauthorized - @WillBuyer"
    abort(401, error=error)


@bplogin.app_errorhandler(MissingCodeError)
@bplogin.app_errorhandler(MismatchingStateError)
def missing_mismatching_state_error(error):
    return redirect(url_for("google.login"))


@bplogin.app_errorhandler(InvalidGrantError)
def invalid_grant_error(error):
    bplogin.session.post(
        "https://accounts.google.com/o/oauth2/revoke",
        params={"token": bplogin.token["access_token"]},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    return redirect(url_for("google.login"))
