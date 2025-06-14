from fastapi import APIRouter, Request, Depends
from app.services.move_service import calculate_next_move
from app.services.move_service import LLMManager

move_router = APIRouter(prefix="/move", tags=["moves"])


def get_llm_manager(request: Request) -> LLMManager:
    return request.app.state.llm_manager


@move_router.get("/move/{move}")
async def get_next_move(move: str, LLMManager=Depends(get_llm_manager)):
    return calculate_next_move(LLMManager, move)
