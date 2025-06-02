import enum
import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy import Column, DateTime, ForeignKey, Enum
from sqlalchemy.sql.sqltypes import String

from app.models.base import Base

class GameStatus(enum.Enum):
    waiting = "waiting"
    active = "active"
    finished = "finished"

class Games(Base):
    __tablename__ = "games"

    sid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    player1_sid = Column(UUID(as_uuid=True), ForeignKey("players.sid"), nullable=False)
    player2_sid = Column(UUID(as_uuid=True), ForeignKey("players.sid"), nullable=False)
    board_player1 = Column(String, nullable=False)
    board_player2 = Column(String, nullable=False)
    status = Column(Enum(GameStatus), default=GameStatus.waiting, nullable=False)
    winner_sid = Column(UUID(as_uuid=True), ForeignKey("players.sid"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
