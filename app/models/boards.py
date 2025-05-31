from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base

class Board(Base):
    __tablename__ = "boards"

    id = Column(Integer, primary_key=True)
    game_sid = Column(UUID(as_uuid=True), ForeignKey("games.sid"))
    player_sid = Column(UUID(as_uuid=True), ForeignKey("players.sid"))
    layout = Column(String, nullable=False)

    game = relationship("Game", back_populates="boards")
    player = relationship("Player")