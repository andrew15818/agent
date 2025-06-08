import dotenv
import chess
from fastapi import APIRouter, Request, Depends
from app.services.move_service import get_next_move

move_router = APIRouter(prefix="/move", tags=["moves"])


@move_router.get("/move")
async def get_next_move(request: Request):
    print(request)
    return {"message": "scholar's mate :D"}
    # return get_next_move(request.headers["move"])
    pass
