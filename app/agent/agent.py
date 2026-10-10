import logging
import chess

from typing import Optional
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_ollama import ChatOllama

from app.agent.prompts import SYSTEM_PROMPT, format_user_prompt
from app.schemas.move_schemas import AgentMove, MoveSchema
from app.schemas.game_schemas import GameStatus, GameColors, GameOutcome
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
        # TODO:
        model = ChatOllama(model=model_id, temperature=0.2)
        self.board_manager = BoardManager()

        # TODO: Figure out how to move tool definition outside of this area.
        # TODO: Validate move even outside the LLM
        @tool
        def is_move_legal(move: AgentMove) -> bool:
            """
            Check whether a move is legal given the current board. The function returns a Boolean
            which confirms the move validity.
            Args:
                move (AgentMove): User or agent move played
            returns:
                Bool: True if the move san is currently valid, False otherwise.
            """
            logger.info("Checking move validity")
            return self.board_manager.check_move_legality(move_san=move.move_san)

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
            move = self.get_agent_move()
            self.board_manager.add_move(move.value)

    def add_move(self, move: MoveSchema) -> bool:
        """
        Add a move to the history, could be user move or agent move.
        Args:
            move (MoveSchema): Move to be played either by agent or user.
        Raises:
            HTTPException if the move is illegal.
        """
        return self.board_manager.add_move(str(move.value))

    def make_ply(self, move: MoveSchema, color: GameColors):
        """
        Make a single move for either the user or agent.
        """
        if not self.add_move(move):
            logger.error(f"Could not add move {move} for player {color.value}")

        pass

    def resolve_game_outcome(self, outcome: chess.Outcome) -> GameOutcome:
        # TODO: Fill this out later for more complex end-status parsing
        """
        Properly parse the chess.Outcome, i.e. a wrapper around chess.Outcome.
        outcome (chess.Outcome):
        """
        return GameOutcome(winner=GameColors.white, reason="No particular reason :^3")
        pass

    def check_game_outcome(self) -> Optional[GameOutcome]:
        """
        Check if the game is over from the board manager.
        """
        outcome = self.board_manager.check_game_outcome()
        if outcome is None:
            return

        # TODO: Further game-over logic
        logger.info(f"Outcome: {outcome}")
        winner = GameColors.white if outcome.winner == chess.WHITE else GameColors.black
        return GameOutcome(winner=winner, reason="Hello there:D")

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
        logger.debug(f"Result coming from LLM: {result}")
        # TODO: Sometimes small models don't include structured response
        structured = result["structured_response"]
        logger.info(f"Structured response: {structured}")
        move = (
            structured.move_san
            if structured
            else str(self.board_manager.get_random_move())
        )
        comment = (
            structured.comment if structured else "What a move (placeholder comment)",
        )
        logger.info(f"Model response: move: {move} \t comment: {comment}")
        agent_move = MoveSchema(value=move, comment=str(comment[0]))
        return agent_move

    def run(self, user_move: MoveSchema) -> MoveSchema | GameOutcome:
        """
        Entry point for the agent loop. While the game is active, run a move and return it to the user.
        Args:
            player_move (MoveSchema): Move made by player
        Returns:
            MoveSchema containing agent move, comment, and current game status
        """
        self.make_ply(user_move, self.user_color)

        # TODO: Check for game over here
        outcome = self.check_game_outcome()
        if outcome is not None:
            return outcome

        # Make agent move
        agent_move = self.get_agent_move()
        try:
            self.make_ply(agent_move, self.agent_color)
            outcome = self.check_game_outcome()
            if outcome is not None:
                return outcome

        except Exception as e:
            logger.error(f"Move {agent_move} failed: {e}")

        ## Decide Next Step
        logger.info(f"Returning move: {agent_move}")
        # TODO: Check for game over again
        return agent_move


if __name__ == "__main__":
    from pathlib import Path
    import sys
    from dotenv import load_dotenv

    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("Hello world")
    env_path = Path(__file__).parent.parent.parent / ".env"
    load_dotenv(env_path)
    agent = ChessAgent(user_color=GameColors.white)
    # agent.board_manager.history = ["e4", "e5"]  # , "Qh5", "Nc6", "Bc4", "Nf6"]
    for move in ["e4", "e5", "Qh5", "Nc6", "Bc4", "Nf6"]:
        agent.board_manager.add_move(move)
        print(f"{agent.board_manager.get_history()}")
    agent.run(user_move=MoveSchema(value="Qxf7", comment="Hello:D"))
