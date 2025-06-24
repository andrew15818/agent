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
    def test_llm_manager_init(self, mock_init_chat_model):
        """Ensure the LLMManager class initializes properly"""
        mock_llm = Mock()
        mock_init_chat_model.return_value = mock_llm

        llm_manager = LLMManager()
        assert llm_manager.color == "black", "LLM Manager should have "

    def test_query_next_move(self):
        """Ensure proper llm calling and error-handling"""
        pass


def test_calculate_next_move():
    """Test the move service's calcualation of the next move."""
    scholars_mate_sequence = ["e4", "e5", "Qh5", "Nc6", "Bc4", "Nf6", "Qxf7"]
    # TODO: Pass the move sequence to the LLM
    pass
