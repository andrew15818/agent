import logging
import os
import json
import logging

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_ollama import ChatOllama

from app.agent.prompts import SYSTEM_PROMPT, USER_PROMPT, format_user_prompt
from app.schemas.move_schemas import AgentMove, MoveSchema
from app.schemas.game_schemas import GameStatus, GameColors
from app.services.board_manager import BoardManager

logger = logging.getLogger(__name__)


class ChessAgent:
    def __init__(
        self,
        user_color: GameColors = GameColors.white,
        model_id: str = "qwen3.5:4b",
    ):
        """
        Create new agent and initializes new game, setting the user and agent colors as indicated.
        """
        model = ChatOllama(model=model_id, temperature=0.2)
        self.board_manager = BoardManager()

        # TODO: Figure out how to move tool definition outside of this area.
        # TODO: Validate move even outside the LLM
        @tool
        def is_move_legal(self, move: AgentMove) -> bool:
            """
            Check user or agent move for legality.
            Args:
                move (AgentMove): User or agent move played
            returns:
                Bool: True if the move san is currently valid, False otherwise.
            """
            is_legal = self.board_manager.check_move_legality(move_san=move.move_san)
            logger.info(f"Is move {move.move_san} legal: {is_legal}")
            return is_legal

        self.is_move_legal = is_move_legal
        self.agent = create_agent(
            model=model,
            tools=[self.is_move_legal],
            response_format=AgentMove,
            system_prompt=SYSTEM_PROMPT,
        )

        self.game_status = GameStatus.ongoing
        self.initialize_new_game(user_color=user_color)

        logger.info("Started new game")

    def initialize_new_game(self, user_color: GameColors) -> None:
        """
        Initialize new game, and set the  agent and user colors.
        Args:
            user_color (GameColors): Color of the user, agent_color will be determined from this.
        """
        self.user_color = user_color
        self.agent_color = (
            GameColors.white if user_color == GameColors.black else GameColors.black
        )
        assert self.user_color != self.agent_color, (
            f"User color ({self.user_color}) should be different than agent color {self.agent_color}"
        )
        logger.info(
            f"Starting agent with agent color {self.agent_color} and user color: {self.user_color}"
        )
        self.board_manager.reset_board()
        if self.agent_color == GameColors.white:
            logger.info(f"Will play first move since agent is {self.agent_color}.")
            self.get_agent_move()

    def add_move(self, move: MoveSchema) -> None:
        """
        Add a move to the history, could be user move or agent move.
        Args:
            move (MoveSchema): Move to be played either by agent or user.
        Raises:
            HTTPException if the move is illegal.
        """
        self.board_manager.add_move(move.value)

    def get_agent_move(self) -> MoveSchema:
        """
        Perform inference on the LLM to obtain the next move from the model.
        """
        user_prompt = format_user_prompt(
            self.board_manager.get_history(), color=self.board_manager.turn
        )
        result = self.agent.invoke(
            {"messages": [{"role": "user", "content": user_prompt}]}
        )
        move, comment = (
            result.get(
                result["structured_response"].move_san,
                str(self.board_manager.get_random_move()),
            ),
            result.get(
                result["structured_response"].comment,
                "What a move (placeholder comment)",
            ),
        )
        logger.info(f"Model response: move: {move} \t comment {comment}")
        agent_move = MoveSchema(value=move, comment=comment)
        self.add_move(agent_move)
        return agent_move

    def run(self, user_move: MoveSchema) -> MoveSchema:
        """
        Entry point for the agent loop. While the game is active, run a move and return it to the user.
        Args:
            player_move (MoveSchema): Move made by player
        Returns:
            MoveSchema containing agent move, comment, and current game status
        """
        ## Validate user move
        self.add_move(user_move)

        agent_move = self.get_agent_move()

        while not self.board_manager.check_move_legality(move_san=agent_move.value):
            logger.info(f"Move {agent_move} is not legal, trying again.")
            break

        try:
            self.board_manager.add_move(agent_move)
        except Exception as e:
            logging.error(f"Move {agent_move} failed with error {e}")

        ## Decide Next Step
        logger.info(f"Returning move: {agent_move}")
        return agent_move


if __name__ == "__main__":
    from pathlib import Path

    from dotenv import load_dotenv

    env_path = Path(__file__).parent.parent.parent / ".env"
    load_dotenv(env_path)
    agent = ChessAgent()
    agent.initialize_new_game(user_color=GameColors.black)
    agent.run(user_move=MoveSchema(value="e4", comment="Hello:D"))
