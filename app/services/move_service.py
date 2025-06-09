import chess
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from google import genai


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
