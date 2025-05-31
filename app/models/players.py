import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import Base


class Players(Base):
    __tablename__ = 'players'
    sid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    games_as_player1 = relationship('Games', back_populates="player1", foreign_keys='Games.player1_sid')
    games_as_player2 = relationship('Games', back_populates="player2", foreign_keys='Games.player2_sid')