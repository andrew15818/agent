from pydantic import BaseModel
from fastapi import Request


# Standard for communicating move between frontend/backend
class MoveSchema(BaseModel):
    value: str
    comment: str
    game_status: str
