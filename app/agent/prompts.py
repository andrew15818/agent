from app.schemas.game_schemas import GameColors

SYSTEM_PROMPT = """
You are an expert chess player with a snarky attitude playing a chess game against a human opponent as either black or white. 
Your task is to generate the next chess move in a game given a sequence of moves.
After choosing the best move, you are to return it as JSON to the player.
"""
USER_PROMPT = """
The move history so far is:

{move_history}

Your task is to choose the best move for {color}.
Pay attention to captures, checks and checkmate threats present from the move history.
The next move is:
"""


def format_user_prompt(move_history: list, color: GameColors):
    assert color in GameColors, (
        f"{color} is not one of the valid colors {GameColors.__members__.keys}"
    )
    return USER_PROMPT.format(move_history=move_history, color=color)
