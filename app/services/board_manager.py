import random
from typing import Optional

import chess
import logging
from fastapi import HTTPException

from app.schemas.game_schemas import GameColors

logger = logging.getLogger(__name__)


class BoardManager:
    """
    Manage the game board via the chess library.
    """

    def __init__(self):
        self.board = chess.Board()
        self.history = []
        self.turn = GameColors.white

    def add_move(self, move: str) -> bool:
        """Check if the move is valid and append it to board.
        Args:
            move (str): Move to add
        Returns:
            bool, True if move is valid, False otherwise
        Raises:
            HTTP Exception if move is invalid.
        """
        try:
            move = str(move)
            self.board.push_san(move)
            self.history.append(move)
            self.turn = (
                GameColors.black if self.turn == GameColors.white else GameColors.white
            )
            logger.info(f"Added move {move} to board history")
            logger.debug(f"History so far: {self.get_history()}")
            return True
        except Exception as e:
            logger.info(
                f"Failed to add move {move} to board given history {self.history}: {e}"
            )
            return False
        return True

    def reset_board(self) -> None:
        """
        Reset the board for starting a new game
        """
        self.board.reset()

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

    def get_random_move(self) -> chess.Move:
        """
        Get a random legal move from the set of legal moves.

        Returns:
            str: Algebraic notation of the random move.
        """
        return random.choice(([move for move in self.board.legal_moves]))

    def check_move_legality(self, move_san: str):
        try:
            self.board.parse_san(move_san)
            return True
        except ValueError:
            # covers InvalidMoveError, IllegalMoveError, AmbiguousMoveError
            return False
