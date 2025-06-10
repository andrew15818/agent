import chess
from fastapi import APIRouter, Request
from app.services.move_service import calculate_next_move

move_router = APIRouter(prefix="/move", tags=["moves"])


@move_router.get("/move/{move}")
async def get_next_move(request: Request, move: str):
    move_history = request.app.state.move_history
    request.app.state.prompt_template.invoke({"color": "white", "move_history": move})
    return calculate_next_move(move_history, move)
