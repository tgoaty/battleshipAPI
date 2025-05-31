from fastapi import APIRouter
from .players import router as players_router
from .games import router as games_router
from .websockets import router as websocket_router

router = APIRouter()

router.include_router(players_router)
router.include_router(games_router)
router.include_router(websocket_router)