from factory import Faker, Sequence
from factory.alchemy import SQLAlchemyModelFactory

from ...model import User


class UserFactory(SQLAlchemyModelFactory):
    provider = "google"
    provider_user_id = Sequence(lambda n: "userid%s" % n)
    email = Faker("email")
    name = Faker("name")
    picture = Faker("image_url")

    class Meta:
        model = User
