from langchain import create_agent
from app.services.move_service import BoardManager
from app.agent.prompts import SYSTEM_PROMPT, USER_PROMPT
from app.schemas.move_schemas import AgentMove

import logging


class ChessAgent:
    def __init__(self, model_id: str = "qwen3.5-4b"):
        # TODO: Add tools to check the move legality
        self.agent = create_agent(model=model_id, tools=[], system_prompt=SYSTEM_PROMPT)
        self.board_manager = BoardManager()

    def start_new_game(self) -> None:
        """
        Initialize new game, clear move history.
        """
        return

    def run(self):
        """
        Placeholder to execute the agent loop.
        """
        pass


if __name__ == "__main__":
    agent = ChessAgent()
