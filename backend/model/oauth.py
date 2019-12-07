from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
from sqlalchemy import Column, BigInteger, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

from ..dao.postgres_db import Base


class OAuth(OAuthConsumerMixin, Base):
    __tablename__ = "oauth"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(UUID(as_uuid=True), unique=True, nullable=False, default=uuid4)
    provider_user_id = Column(String(256), nullable=False)
    provider = Column(String(50), nullable=False)
    user_id = Column(BigInteger, ForeignKey("user.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    user = relationship("User", back_populates="oauth")

    __table_args__ = tuple(
        UniqueConstraint(provider_user_id, provider)
    )
