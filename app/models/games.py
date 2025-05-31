import enum
import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy import Column, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship

from app.models.base import Base

class GameStatus(enum.Enum):
    waiting = "waiting"
    active = "active"
    finished = "finished"

class Games(Base):
    __tablename__ = 'games'
    sid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    player1_sid = Column(UUID(as_uuid=True), ForeignKey('players.sid'))
    player2_sid = Column(UUID(as_uuid=True), ForeignKey('players.sid'))
    winner_sid = Column(UUID(as_uuid=True), ForeignKey('players.sid'), nullable=True)
    status = Column(Enum(GameStatus), default=GameStatus.waiting)
    created_at = Column(DateTime, default=datetime.utcnow)

    player1 = relationship("Player", foreign_keys=[player1_sid], back_populates="games_as_player1")
    player2 = relationship("Player", foreign_keys=[player2_sid], back_populates="games_as_player2")
    moves = relationship("Move", back_populates="game")
    boards = relationship("Board", back_populates="game")