from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class Move(Base):
    __tablename__ = "moves"

    id = Column(Integer, primary_key=True)
    game_sid = Column(UUID(as_uuid=True), ForeignKey("games.sid"))
    player_sid = Column(UUID(as_uuid=True), ForeignKey("players.sid"))
    x = Column(Integer)
    y = Column(Integer)
    hit = Column(Boolean)
    created_at = Column(DateTime, default=datetime.utcnow)

    game = relationship("Game", back_populates="moves")
    player = relationship("Player")