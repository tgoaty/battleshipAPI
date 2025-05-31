from fastapi import APIRouter

router = APIRouter(tags=["websocket"])

@router.websocket("/games/{game_id}/play")
async def websocket_endpoint():
    pass
