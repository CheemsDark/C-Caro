from core.board import Board
from ai.agent import AIAgent

class GameEngine:
    def __init__(self, size=9, ai_algorithm="alpha_beta", ai_depth=3, ai_player=Board.PLAYER_O, human_player=Board.PLAYER_X):
        self.board = Board(size)
        self.ai_player = ai_player
        self.human_player = human_player
        self.ai = AIAgent(algorithm=ai_algorithm, depth=ai_depth, ai_player=ai_player, human_player=human_player)
        self.current_player = Board.PLAYER_X # Người luôn đi trước (X)
        self.status = "ongoing" # "ongoing", "x_won", "o_won", "draw"

    def make_human_move(self, row, col):
        if self.current_player != self.human_player or self.status != "ongoing":
            return False
            
        if self.board.make_move(row, col, self.human_player):
            self._check_status()
            if self.status == "ongoing":
                self.current_player = self.ai_player
            return True
        return False

    def make_ai_move(self):
        if self.current_player != self.ai_player or self.status != "ongoing":
            return None
            
        # Truyền bản sao của bàn cờ để AI mô phỏng không làm ảnh hưởng giao diện (sửa lỗi nhấp nháy)
        result = self.ai.get_move(self.board.copy())
        if result["move"]:
            r, c = result["move"]
            self.board.make_move(r, c, self.ai_player)
            self._check_status()
            if self.status == "ongoing":
                self.current_player = self.human_player
        return result

    def _check_status(self):
        if self.board.check_win(Board.PLAYER_X):
            self.status = "x_won"
        elif self.board.check_win(Board.PLAYER_O):
            self.status = "o_won"
        elif self.board.is_full():
            self.status = "draw"
