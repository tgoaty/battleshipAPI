from fastapi import APIRouter

router = APIRouter(prefix="/players", tags=["players"])

@router.post("/register")
async def register_player():
    pass


@router.post("/login")
async def login_player():
    pass

@router.get("")
async def get_available_players():
    pass


@router.get("/{player_sid}/stats")
async def get_player_stats():
    pass