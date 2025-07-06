from pydantic import BaseModel
from enum import Enum


class GameStatus(str, Enum):
    not_started = "not_started"
    ongoing = "ongoing"
    finished = "finished"


# Standard for communicating move between frontend/backend
class MoveSchema(BaseModel):
    value: str
    comment: str = ""
    game_status: GameStatus = GameStatus.not_started
