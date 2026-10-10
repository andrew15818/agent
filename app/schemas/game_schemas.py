from enum import Enum
from pydantic import BaseModel


class GameStatus(str, Enum):
    not_started = "not_started"
    ongoing = "ongoing"
    finished = "finished"


class GameColors(int, Enum):
    white = 0
    black = 1

    def __str__(self):
        return self.name


class GameOutcome(BaseModel):
    winner: GameColors
    reason: str
