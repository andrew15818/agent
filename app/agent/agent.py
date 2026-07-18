import logging
import os

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_ollama import ChatOllama

from app.agent.prompts import SYSTEM_PROMPT, USER_PROMPT, format_user_prompt
from app.schemas.move_schemas import AgentMove
from app.schemas.game_schemas import GameStatus, GameColors
from app.services.move_service import BoardManager


class ChessAgent:
    def __init__(self, model_id: str = "qwen3.5:4b"):
        model = ChatOllama(model=model_id, temperature=0.2)
        self.agent = create_agent(
            model=model,
            tools=[self.is_move_legal],
            response_format=AgentMove,
            system_prompt=SYSTEM_PROMPT,
        )
        self.board_manager = BoardManager()
        self.game_status = GameStatus

    def start_new_game(self) -> None:
        """
        Initialize new game, clear move history.
        """
        self.board_manager.reset_board()

    def run(self):
        """
        Entry point for the agent harness. While the game is active, run a move and return it to the user.

        """
        while self.game_status != GameStatus.finished:
            user_prompt = format_user_prompt(
                self.board_manager.get_history(), color=self.board_manager.turn
            )
            result = self.agent.invoke(
                {"messages": [{"role": "user", "content": user_prompt}]}
            )
            print(result)
            break

    @tool
    def is_move_legal(self, move: AgentMove) -> bool:
        """
        Check move legality
        """
        return True


if __name__ == "__main__":
    from pathlib import Path

    from dotenv import load_dotenv

    env_path = Path(__file__).parent.parent.parent / ".env"
    load_dotenv(env_path)
    agent = ChessAgent()
    agent.start_new_game()
    agent.run()
