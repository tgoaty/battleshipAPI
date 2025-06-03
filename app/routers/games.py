from fastapi import APIRouter

from app.database import get_db
from app.models.games import Games
from app.schemes.games import GameStatus, GameOut, GameCreate
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.utils.board_generator import generate_board

router = APIRouter(prefix="/games", tags=["games"])


@router.post("/create", response_model=GameOut)
async def create_game(data: GameCreate, db: AsyncSession = Depends(get_db)):
    if data.player1_sid == data.player2_sid:
        raise HTTPException(status_code=400, detail="Players must be different")

    new_game = Games(
        player1_sid=data.player1_sid,
        player2_sid=data.player2_sid,
        board_player1=generate_board(),
        board_player2=generate_board(),
        status=GameStatus.waiting,

    )
    db.add(new_game)
    await db.commit()
    await db.refresh(new_game)
    return new_game


@router.get("", response_model=list[GameOut])
async def get_active_games(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Games).where(Games.status.in_([GameStatus.waiting, GameStatus.active])))
    games = result.scalars().all()
    return games
