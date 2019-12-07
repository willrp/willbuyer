from sqlalchemy.exc import DatabaseError

from backend.model import User, OAuth
from backend.dao.postgres_db import DBSession


class UserService(object):
    def __init__(self):
        self.db_session = DBSession()

    def get_create_oauth(self, provider: str, provider_user_id: int, token: dict) -> OAuth:
        query = self.db_session.query(OAuth).filter_by(provider=provider, provider_user_id=provider_user_id)
        oauth = query.one_or_none()
        if oauth is None:
            oauth = OAuth(provider=provider, provider_user_id=provider_user_id, token=token)

        return oauth

    def get_create_user(self, oauth: OAuth, email: str, name: str, picture: str) -> User:
        provider = oauth.provider
        provider_user_id = oauth.provider_user_id
        query = self.db_session.query(User).filter_by(provider=provider, provider_user_id=provider_user_id)
        try:
            user = query.one_or_none()
            if user is None:
                user = User(provider=provider, provider_user_id=provider_user_id, email=email, name=name, picture=picture)
            else:
                user.name = name
                user.picture = picture

            oauth.user = user
            self.db_session.add_all([user, oauth])
            self.db_session.commit()
        except DatabaseError:
            self.db_session.rollback()
            raise

        return user
