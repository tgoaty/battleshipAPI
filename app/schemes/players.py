from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field
from app.models.games import GameStatus


class PlayerRegister(BaseModel):
    username: str
    password: str


class PlayerLogin(BaseModel):
    username: str
    password: str


class PlayerOut(BaseModel):
    sid: UUID
    username: str

    class Config:
        orm_mode = True


class PlayerGameStats(BaseModel):
    game_sid: UUID = Field(..., alias="sid")
    player1_sid: UUID
    player2_sid: UUID
    board_player1: str
    board_player2: str
    status: GameStatus
    winner_sid: Optional[UUID] = None
    created_at: datetime
    current_turn_sid: Optional[UUID] = None

    class Config:
        from_attributes = True
        allow_population_by_field_name = True
