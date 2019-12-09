from flask import Blueprint
from flask_restplus import Api


bpapi = Blueprint("api", __name__)

authorizations = {
    "login": {
        "type": "oauth2",
        "flow": "authorizationCode",
        "authorizationUrl": "/auth/login/"
    },
    "logout": {
        "type": "oauth2",
        "flow": "authorizationCode",
        "authorizationUrl": "/auth/logout/"
    }
}

api = Api(bpapi,
    title="WillBuyer API",
    description="WillBuyer API - Back end.",
    version="0.0.1",
    doc="/",
    authorizations=authorizations
)

api.namespaces.clear()

from .cart import NSCart

for ns in NSCart:
    api.add_namespace(ns, path="/cart")

from .order import NSOrder

for ns in NSOrder:
    api.add_namespace(ns, path="/order")

from .store import NSStore

for ns in NSStore:
    api.add_namespace(ns, path="/store")

from .user import NSUser

for ns in NSUser:
    api.add_namespace(ns, path="/user")
