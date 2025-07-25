import json
import os
import random
from typing import Optional

import chess
from dotenv import load_dotenv
from fastapi import HTTPException
from google import genai
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate

from app.schemas.move_schemas import GameStatus, MoveSchema


class LLMManager:
    """Group LLM-related methods together in a single class."""

    def __init__(self, color: str = "black"):
        self.board_manager = BoardManager()
        self.llm = init_chat_model(os.getenv("MODEL_NAME"), model_provider="mistralai")
        self.color = color  # TODO: Better manage the color choice.
        self.system_prompt = os.getenv("SYSTEM_PROMPT")
        self.human_prompt = os.getenv("HUMAN_PROMPT")
        print(self.human_prompt)
        self.prompt_template = ChatPromptTemplate(
            [
                ("system", self.system_prompt),
                ("human", self.human_prompt),
            ]
        )
        self.prompt_template.invoke(
            {
                "color": self.color,
                "move_history": "[]",
                "move": self.board_manager.get_history(),
            }
        )
        self.chain = self.prompt_template | self.llm

        print(type(self.chain))
        print(f"System prompt: {self.system_prompt}")

    def query_next_move(self, move_played: MoveSchema) -> MoveSchema:
        """Query the LLM for the next move using the history of moves.
        Args:
            move (str): Move just made.
        """
        move = move_played.value
        self.board_manager.add_move(move)
        history = self.board_manager.get_history()
        print(f"History so far: {history}")

        # Update prompt with new history
        response = self.chain.invoke(
            {
                "color": self.color,
                "move_history": " ".join(history),
                "move": move,
            }
        )

        # TODO: Handle illegal moves
        try:
            content = json.loads(response.content)
            print(f"Response from LLM: {content}")
            self.board_manager.add_move(content["move"])
        except json.JSONDecodeError:
            # Make random move from now
            content = {
                "move": self.board_manager.get_random_move(),
                "comment": "Probably playing a suboptimal move :(",
            }
            self.board_manager.add_move(move)

        outcome = self.board_manager.check_game_outcome()

        # TODO: rework the value
        if outcome is not None:
            print(f"Game over with status {str(outcome.termination)}")
            return MoveSchema(
                value="game_over",
                comment=str(response.comment),
                game_status=GameStatus.finished,
            )
        return MoveSchema(
            value=content["move"],
            comment=content["comment"],
            game_status=GameStatus.ongoing,
        )


class BoardManager:
    """
    Manage the game board via the chess library.
    """

    def __init__(self):
        self.board = chess.Board()
        self.history = []

    def add_move(self, move: str) -> None:
        """Check if the move is valid and append it to board.
        Args:
            move (str): Move to add
        Returns:
            None, if  move is valid.
        Raises:
            HTTP Exception if move is invalid.
        """
        try:
            self.board.push_san(move)
        except chess.InvalidMoveError:
            raise HTTPException(status_code=501, detail=f"Move {move} is invalid.")

        self.history.append(move)

    def get_history(self) -> list[str]:
        return self.history

    def check_game_outcome(self) -> Optional[chess.Outcome]:
        """
        Check if the game is over or has any other special situation.
        Returns:
            chess.Outcome object if game is terminated, `None` otherwise.
        """
        return self.board.outcome()

    def get_board_status(self) -> str:
        return self.board.__str__()

    def get_random_move(self) -> str:
        """
        Get a random legal move from the set of legal moves.

        Returns:
            str: Algebraic notation of the random move.
        """
        return random.choice(list(self.board.legal_moves))


def calculate_next_move(llm_manager: LLMManager, move_played: MoveSchema) -> MoveSchema:
    """Get the next move from the LLM given the move history.

    Args:
        llm_manager (LLMManager): Object managing LLM state info and connection.
        move_played (str): Move just made by player.
    Returns:
        str: The next move in algebraic notation.
    """
    print(type(llm_manager), move_played)
    move = llm_manager.query_next_move(move_played)

    return move


def check_if_move_is_valid() -> None:
    pass


if __name__ == "__main__":
    env = load_dotenv()
    # Test connection to Gemini API
    client = genai.Client()
    pass
