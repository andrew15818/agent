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
