from pydantic import BaseModel


# Standard for communicating move between frontend/backend
class MoveSchema(BaseModel):
    value: str
    comment: str = ""
    game_status: str = "ongoing"
