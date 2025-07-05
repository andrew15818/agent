from fastapi import APIRouter, Request, Depends
from app.services.move_service import calculate_next_move
from app.services.move_service import LLMManager
from app.schemas.move_schemas import MoveSchema

move_router = APIRouter(prefix="/move", tags=["moves"])


def get_llm_manager(request: Request) -> LLMManager:
    return request.app.state.llm_manager


@move_router.post("/move")
async def get_next_move(move: MoveSchema, LLMManager=Depends(get_llm_manager)):
    return calculate_next_move(LLMManager, move)


@move_router.get("/show_board")
async def show_board(LLMManager=Depends(get_llm_manager)) -> str:
    return LLMManager.board_manager.get_board_status()
