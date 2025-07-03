from unittest.mock import MagicMock, Mock, patch

import pytest
from fastapi.testclient import TestClient

from app.services.move_service import BoardManager, LLMManager, calculate_next_move


class TestBoardManager:
    pass


class TestLLMManager:
    """Test LLMManager initialization and next move generation"""

    @patch.dict(
        {
            "MODEL_NAME": "mistral-small",
            "SYSTEM_PROMPT": "You are a professional chess player playing as {color}. Given the move history, your task is to generate the best move given the context, and return it as a JSON object.",
            "HUMAN_PROMPT": "Given the move history {move_history}, play the best legal move and return your answer as json: ",
        }
    )
    @patch("app.services.move_service.init_chat_model")
    def test_llm_manager_init(self, mock_init_chat_model, setup_env_vars):
        """
        Ensure the LLMManager class initializes properly, mocking the chat MODEL_NAME
        and environment variables.
        """
        mock_llm = Mock()
        mock_init_chat_model.return_value = mock_llm

        llm_manager = LLMManager()
        assert llm_manager.color == "black", (
            "LLM Manager should be playing black (for now)"
        )

    def test_query_next_move(self):
        """Ensure proper llm calling and error-handling"""
        pass


@patch("app.services.move_service.init_chat_model")
def test_calculate_next_move(mock_init_chat_model, setup_env_vars):
    """Test the move service's calcualation of the next move."""

    # TODO: Mock the LLM call and response

    mock_llm = Mock()
    mock_init_chat_model.return_value = mock_llm

    llm_manager = LLMManager()
    move_played = "e4"
    response = llm_manager.query_next_move(move_played)
    assert isinstance(response, dict), (
        "Response from `query_next_move` should be a dictionary!"
    )

    # TODO: Pass the move sequence to the LLM
    scholars_mate_sequence = ["e4", "e5", "Qh5", "Nc6", "Bc4", "Nf6"]
    llm_manager.board_manager.history = scholars_mate_sequence

    result = llm_manager.query_next_move("Qxf7")  # Should be checkmate
    assert isinstance(result, dict), "Result should be dict after checkmate."
