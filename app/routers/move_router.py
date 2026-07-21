from fastapi import APIRouter, Request, Depends
from app.services.move_service import calculate_next_move
from app.agent.agent import ChessAgent
from app.schemas.move_schemas import MoveSchema

move_router = APIRouter(prefix="/move", tags=["moves"])


def get_agent(request: Request) -> ChessAgent:
    return request.app.state.agent


@move_router.post("/start_game")
async def start_game(request: Request, color: str = "black"):
    request.app.state.agent = ChessAgent(color)


@move_router.post("/move")
async def get_next_move(move: MoveSchema, LLMManager=Depends(get_agent)):
    return calculate_next_move(LLMManager, move)


@move_router.get("/show_board")
async def show_board(LLMManager=Depends(get_agent)) -> str:
    return LLMManager.board_manager.get_board_status()
