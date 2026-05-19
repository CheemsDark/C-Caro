from ai.minimax import MinimaxAI
from ai.alpha_beta import AlphaBetaAI
from core.board import Board

class AIAgent:
    def __init__(self, algorithm="alpha_beta", depth=3, ai_player=Board.PLAYER_O, human_player=Board.PLAYER_X):
        self.algorithm = algorithm
        self.depth = depth
        if algorithm == "minimax":
            self.engine = MinimaxAI(ai_player=ai_player, human_player=human_player)
        elif algorithm == "alpha_beta":
            self.engine = AlphaBetaAI(ai_player=ai_player, human_player=human_player)
        else:
            raise ValueError("Algorithm must be 'minimax' or 'alpha_beta'")

    def get_move(self, board: Board):
        """
        Trả về dictionary chứa thông tin chi tiết về nước đi được chọn.
        """
        move, score, nodes, time_ms = self.engine.get_best_move(board, self.depth)
        return {
            "move": move,
            "score": score,
            "nodes": nodes,
            "time_ms": time_ms
        }
