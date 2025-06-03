import json
from fastapi import WebSocket, WebSocketDisconnect, APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from app.database import get_db
from app.models.games import Games, GameStatus

router = APIRouter(tags=["websocket"])

connections: dict[UUID, dict[UUID, WebSocket]] = {}


@router.websocket("/games/{game_sid}/play")
async def websocket_game(
        websocket: WebSocket,
        game_sid: UUID,
        player_sid: UUID = Query(...),
        db: AsyncSession = Depends(get_db),
):
    await websocket.accept()

    if game_sid not in connections:
        connections[game_sid] = {}
    connections[game_sid][player_sid] = websocket

    result = await db.execute(select(Games).where(Games.sid == game_sid))
    game: Games = result.scalar()

    if not game or player_sid not in [game.player1_sid, game.player2_sid]:
        await websocket.send_text(json.dumps({"error": "Invalid player or game"}))
        await websocket.close()
        return

    if len(connections[game_sid]) == 2 and game.status == GameStatus.waiting:
        game.status = GameStatus.active
        game.current_turn_sid = game.player1_sid
        await db.commit()

        for sid, ws in connections[game_sid].items():
            await ws.send_text(json.dumps({
                "type": "start",
                "your_sid": str(sid),
                "first_turn": str(game.player1_sid)
            }))

    def get_opponent_board(g: Games, sid: UUID) -> str:
        return g.board_player2 if sid == g.player1_sid else g.board_player1

    def set_opponent_board(g: Games, sid: UUID, new_board: str):
        if sid == g.player1_sid:
            g.board_player2 = new_board
        else:
            g.board_player1 = new_board

    def all_ships_sunk(board: str) -> bool:
        return '1' not in board

    try:
        while True:
            msg = await websocket.receive_text()
            data = json.loads(msg)

            if data["type"] == "move":
                await db.refresh(game)
                if player_sid != game.current_turn_sid:
                    await websocket.send_text(json.dumps({"error": "Not your turn"}))
                    continue

                x, y = data["x"], data["y"]
                if not (0 <= x < 10 and 0 <= y < 10):
                    await websocket.send_text(json.dumps({"error": "Invalid coordinates"}))
                    continue

                index = y * 10 + x
                board = get_opponent_board(game, player_sid)
                cell = board[index]

                if cell in ["X", "O"]:
                    await websocket.send_text(json.dumps({"error": "Cell already shot"}))
                    continue

                hit = cell == "1"
                board = board[:index] + ("X" if hit else "O") + board[index + 1:]
                set_opponent_board(game, player_sid, board)
                await db.commit()

                if all_ships_sunk(board):
                    game.status = GameStatus.finished
                    game.winner_sid = player_sid
                    await db.commit()
                    for ws in connections[game_sid].values():
                        await ws.send_text(json.dumps({
                            "type": "end",
                            "winner_sid": str(player_sid)
                        }))
                    break

                game.current_turn_sid = (
                    game.player2_sid if player_sid == game.player1_sid else game.player1_sid
                )
                await db.commit()

                for sid, ws in connections[game_sid].items():
                    await ws.send_text(json.dumps({
                        "type": "result",
                        "from": str(player_sid),
                        "x": x,
                        "y": y,
                        "hit": hit,
                        "next_turn": str(game.current_turn_sid)
                    }))

    except WebSocketDisconnect:
        connections[game_sid].pop(player_sid, None)
