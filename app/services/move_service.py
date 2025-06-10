import os

import chess
from dotenv import load_dotenv
from google import genai
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool


class LLMManager:
    """
    Group LLM-related methods together in a single class.
    """

    def __init__(self):
        self.llm = init_chat_model(os.getenv("MODEL_NAME"), model_provider="mistralai")
        self.system_prompt = os.getenv("SYSTEM_PROMPT")
        self.move_history = []
        self.prompt_template = ChatPromptTemplate([("system", self.system_prompt)])
        self.prompt_template.invoke(
            {"color": "white", "move_history": self.move_history}
        )
        self.chain = self.prompt_template | self.llm
        print(type(self.chain))
        print(f"System prompt: {self.system_prompt}")

        pass


class BoardManager:
    """
    Manage the game board via the chess library.
    """

    def __init__(self):
        pass


@tool
def calculate_next_move(history: list[str], current_move: str, color: str) -> str:
    """Get the next move from the LLM given the move history.

    Args:
        history (list[str]): The list of moves made so far.
        move (str): The current move played.
        color (str): The color of the current move.
    Returns:
        str: The next move in algebraic notation.
    """

    return "kf3"


def check_if_move_is_valid() -> None:
    pass


if __name__ == "__main__":
    env = load_dotenv()
    # Test connection to Gemini API
    client = genai.Client()
    pass
