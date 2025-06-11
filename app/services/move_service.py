import os

import chess
from dotenv import load_dotenv
from google import genai
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool


class LLMManager:
    """Group LLM-related methods together in a single class."""

    def __init__(self):
        self.llm = init_chat_model(os.getenv("MODEL_NAME"), model_provider="mistralai")
        self.color = "white"
        self.system_prompt = os.getenv("SYSTEM_PROMPT")
        self.move_history = []
        self.prompt_template = ChatPromptTemplate([("system", self.system_prompt)])
        self.prompt_template.invoke(
            {"color": self.color, "move_history": self.move_history}
        )
        self.chain = self.prompt_template | self.llm
        print(type(self.chain))
        print(f"System prompt: {self.system_prompt}")

        pass

    def add_move(self, new_move: str) -> None:
        """Add move to the history_pile
        Args:
         new_move (str): Move to add
        """
        self.move_history.append(new_move)

    def pop_move(self) -> str:
        """Pop move from the history in case not valid.
        Returns:
            str: The move just popped
        """
        return self.move_history.pop()


class BoardManager:
    """
    Manage the game board via the chess library.
    """

    def __init__(self):
        pass


def calculate_next_move(llm_manager: LLMManager, move_played: str) -> str:
    """Get the next move from the LLM given the move history.

    Args:
        llm_manager (LLMManager): Object managing LLM state info and connection.
        move_played (str): Move just made by player.
    Returns:
        str: The next move in algebraic notation.
    """
    print(f"Processing move: {move_played}")
    return "kf3"


def check_if_move_is_valid() -> None:
    pass


if __name__ == "__main__":
    env = load_dotenv()
    # Test connection to Gemini API
    client = genai.Client()
    pass
