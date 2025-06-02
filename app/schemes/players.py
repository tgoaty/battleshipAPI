from uuid import UUID
from pydantic import BaseModel
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
    game_sid: UUID
    created_at: str
    status: GameStatus
    winner_sid: UUID | None

    class Config:
        orm_mode = True