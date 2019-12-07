from flask_login import UserMixin
from datetime import datetime
from sqlalchemy import Column, BigInteger, String, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

from ..dao.postgres_db import Base
from ..util.slug import uuid_to_slug


class User(UserMixin, Base):
    __tablename__ = "user"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(UUID(as_uuid=True), unique=True, nullable=False, default=uuid4)
    provider_user_id = Column(String(256), nullable=False)
    provider = Column(String(50), nullable=False)
    email = Column(String(150), nullable=False)
    name = Column(String(150), nullable=False)
    picture = Column(String(2000), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    oauth = relationship("OAuth", uselist=False, back_populates="user")

    __table_args__ = tuple(
        UniqueConstraint(provider_user_id, provider)
    )

    @property
    def uuid_slug(self):
        return uuid_to_slug(self.uuid)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "email": self.email,
            "picture": self.picture
        }
