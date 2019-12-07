from factory import Sequence
from factory.alchemy import SQLAlchemyModelFactory
from datetime import datetime

from ...model import OAuth


class OAuthFactory(SQLAlchemyModelFactory):
    provider = "google"
    provider_user_id = Sequence(lambda n: "userid%s" % n)
    token = {
        "id_token": "test.id.token",
        "access_token": "test.access.token",
        "refresh_token": "test.refresh.token",
        "expires_in": 3600,
        "token_type": "Bearer",
        "expires_at": (datetime.utcnow().timestamp() + 3600)
    }

    class Meta:
        model = OAuth
