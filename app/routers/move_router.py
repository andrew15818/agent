from fastapi import APIRouter

move_router = APIRouter(prefix="/move", tags=["moves"])


@move_router.get("/move")
async def get_next_move() -> None:
    pass
