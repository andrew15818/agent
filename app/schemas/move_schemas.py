from pydantic import BaseModel
from enum import Enum
from app.schemas.game_schemas import GameStatus


# Standard for communicating move between frontend/backend
class MoveSchema(BaseModel):
    value: str
    comment: str = ""
    game_status: GameStatus = GameStatus.ongoing


class AgentMove(BaseModel):
    move_san: str
    comment: str
