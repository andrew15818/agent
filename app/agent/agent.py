import logging
import os
import json

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_ollama import ChatOllama

from app.agent.prompts import SYSTEM_PROMPT, USER_PROMPT, format_user_prompt
from app.schemas.move_schemas import AgentMove, MoveSchema
from app.schemas.game_schemas import GameStatus
from app.services.board_manager import BoardManager


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

    def add_user_move(self, user_move: MoveSchema) -> None:
        """
        Ensure the move entered by the player is valid, return error if not
        """
        self.board_manager.add_move(user_move.value)

    def run(self, user_move: MoveSchema) -> MoveSchema:
        """
        Entry point for the agent harness. While the game is active, run a move and return it to the user.
        Args:
            player_move (MoveSchema): Move made by player
        Returns:
            MoveSchema containing agent move, comment, and current game status
        """
        ## Validate user move
        self.add_user_move(user_move)

        user_prompt = format_user_prompt(
            self.board_manager.get_history(), color=self.board_manager.turn
        )
        result = self.agent.invoke(
            {"messages": [{"role": "user", "content": user_prompt}]}
        )
        ## Send to Model
        move, comment = (
            result.get(
                result["structured_response"].move_san,
                str(self.board_manager.get_random_move()),
            ),
            result.get(
                result["structured_response"].comment,
                "What a move (placeholder comment)",
            ),
        )
        print(f"Got move {move} and comment {comment}")
        ## Process Model Output
        try:
            self.board_manager.add_move(move)
        except Exception as e:
            logging.error(f"Move {move} failed with error {e}")

        ## Decide Next Step

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
