import json
import os
import random
from typing import Optional

import chess
from app.agent.agent import ChessAgent
from dotenv import load_dotenv
from fastapi import HTTPException
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate

from app.schemas.game_schemas import GameColors, GameStatus
from app.schemas.move_schemas import MoveSchema


class LLMManager:
    """Group LLM-related methods together in a single class."""

    def __init__(self, color: str = "black"):
        self.board_manager = BoardManager()
        self.llm = init_chat_model(os.getenv("MODEL_NAME"), model_provider="mistralai")
        self.color = color  # TODO: Better manage the color choice.
        self.system_prompt = os.getenv("SYSTEM_PROMPT")
        self.user_prompt = os.getenv("USER_PROMPT")
        print(self.user_prompt)
        self.prompt_template = ChatPromptTemplate(
            [
                ("system", self.system_prompt),
                ("human", self.user_prompt),
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


def calculate_next_move(agent: ChessAgent, move_played: MoveSchema) -> MoveSchema:
    """Get the next move from the LLM given the move history.

    Args:
        llm_manager (LLMManager): Object managing LLM state info and connection.
        move_played (str): Move just made by player.
    Returns:
        str: The next move in algebraic notation.
    """
    print(type(agent), move_played)
    # TODO:
    ## Handle User move
    # move = llm_manager.query_next_move(move_played)
    move = agent.run(move_played)
    return move


if __name__ == "__main__":
    env = load_dotenv()
    # Test connection to Gemini API
    client = genai.Client()
    pass
