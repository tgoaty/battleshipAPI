from http.client import HTTPException
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.schemes.players import PlayerOut, PlayerLogin, PlayerRegister
from app.models.players import Players
from app.models.games import Games
from app.models.games import GameStatus


router = APIRouter(prefix="/players", tags=["players"])




@router.post("/register", response_model=PlayerOut)
async def register(data: PlayerRegister, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Players).where(Players.username == data.username))
    if result.scalar():
        raise HTTPException(status_code=400, detail="Username already exists")

    new_player = Players(username=data.username, password=data.password)
    db.add(new_player)
    await db.commit()
    await db.refresh(new_player)
    return new_player

@router.post("/login", response_model=PlayerOut)
async def login(data: PlayerLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Players).where(Players.username == data.username))
    player = result.scalar()
    if not player or player.password != data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return player


@router.get("", response_model=list[PlayerOut])
async def get_available_players(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Players))
    all_players = result.scalars().all()

    result = await db.execute(select(Games))
    games = result.scalars().all()

    busy_ids = set()
    for game in games:
        if game.status in [GameStatus.waiting, GameStatus.active]:
            if game.player1_sid:
                busy_ids.add(game.player1_sid)
            if game.player2_sid:
                busy_ids.add(game.player2_sid)

    available_players = [p for p in all_players if p.sid not in busy_ids]
    return available_players

@router.get("/{player_sid}/stats")
async def get_player_stats():
    pass