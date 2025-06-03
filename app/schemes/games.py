from datetime import datetime
from uuid import UUID
from pydantic import BaseModel

from app.models.games import GameStatus


class GameCreate(BaseModel):
    player1_sid: UUID
    player2_sid: UUID


class GameOut(BaseModel):
    sid: UUID
    player1_sid: UUID
    player2_sid: UUID
    board_player1: str
    board_player2: str
    status: GameStatus
    created_at: datetime

    class Config:
        orm_mode = True
