import os
import pytest
from unittest.mock import patch


@pytest.fixture
def setup_env_vars():
    """Setup environment variables for testing"""

    env_vars = {
        "MODEL_NAME": "mistral-small",
        "MODEL_PROVIDER": "mistralai",
        "SYSTEM_PROMPT": 'You are an expert chess player, playing a chess game as the color {color}.\n You are responsbile for generating a move in algebraic notation given the moves played so far.  \n The moves so far are {move_history}. Generate a first move if your color is white and the move history is empty.\n Return the algebraic notation of your move in JSON code, with the move in the "move" field, and a comment in the "comment" field describing your reasoning.\n Generate the next move in algebraic notation: ',
        "HUMAN_PROMPT": 'The move history is {move_history} and the current move is {move}.\n Play the best next move with the color {color}.\n Pay attention to captures, checks and checkmate threats present from the move history. Return your result in JSON format with the "move" field having the algebraic notation of your move and a "comment" field commenting on your move choice. Even when checkmated, return only a JSON object with the "move" and "comment" fields. The next move is:',
    }
    with patch.dict(os.environ, env_vars, clear=False):
        yield env_vars
