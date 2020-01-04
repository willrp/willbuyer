import asyncio
import requests
from flask import Blueprint, render_template, jsonify, session, redirect, current_app as app
from flask_login import current_user


bpfrontend = Blueprint("frontend", __name__)


@bpfrontend.app_errorhandler(405)
def method_not_allowed(e):
    error = {
        "error": "Method not Allowed - @WillBuyer"
    }
    return jsonify(error), 405


async def wake_up_webservices():
    url = app.config["WILLSTORES_WS"]
    requests.get("%s/api/start" % (url))


@bpfrontend.route("/", methods=['GET'], strict_slashes=False)
@bpfrontend.route("/<path:path>", methods=['GET'], strict_slashes=False)
def index(path=None):
    asyncio.run(wake_up_webservices())

    if session.get("next_url") and current_user.is_authenticated:
        next_url = session.get("next_url")
        session.pop("next_url", None)
        return redirect(next_url)
    else:
        session.pop("next_url", None)
        return render_template("index.html")
