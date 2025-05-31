from fastapi import APIRouter

router = APIRouter(prefix="/games", tags=["games"])

@router.post("/create")
async def create_game():
    pass

@router.get("")
async def get_available_games():
    pass

