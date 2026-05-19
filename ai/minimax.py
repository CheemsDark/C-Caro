from core.board import Board
from ai.evaluator import Evaluator
import math
import time

class MinimaxAI:
    def __init__(self, ai_player=Board.PLAYER_O, human_player=Board.PLAYER_X):
        self.ai_player = ai_player
        self.human_player = human_player
        self.nodes_visited = 0

    def get_best_move(self, board: Board, depth: int):
        self.nodes_visited = 0
        start_time = time.time()
        
        best_score = -math.inf
        best_move = None
        
        valid_moves = board.get_valid_moves()
        if not valid_moves:
            return None, 0, 0, 0
            
        # Thử từng nước đi
        for r, c in valid_moves:
            # Simulate
            board.grid[r][c] = self.ai_player
            board.last_move = (r, c)
            board.move_count += 1
            
            score = self.minimax(board, depth - 1, False)
            
            # Undo
            board.grid[r][c] = Board.EMPTY
            board.move_count -= 1
            board.last_move = None # Simplified, not perfectly accurate undo for last_move but enough for search
            
            if score > best_score:
                best_score = score
                best_move = (r, c)
                
        execution_time = (time.time() - start_time) * 1000 # ms
        return best_move, best_score, self.nodes_visited, execution_time

    def minimax(self, board: Board, depth: int, is_maximizing: bool):
        self.nodes_visited += 1
        
        # Check terminal states
        if board.check_win(self.ai_player):
            return 1000000 + depth # Khuyến khích thắng sớm (depth lớn hơn là ít bước hơn)
        if board.check_win(self.human_player):
            return -1000000 - depth # Tránh thua sớm
        if board.is_full() or depth == 0:
            return Evaluator.evaluate(board, self.ai_player)
            
        if is_maximizing:
            best_score = -math.inf
            for r, c in board.get_valid_moves():
                board.grid[r][c] = self.ai_player
                board.last_move = (r, c)
                board.move_count += 1
                
                score = self.minimax(board, depth - 1, False)
                best_score = max(best_score, score)
                
                board.grid[r][c] = Board.EMPTY
                board.move_count -= 1
            return best_score
        else:
            best_score = math.inf
            for r, c in board.get_valid_moves():
                board.grid[r][c] = self.human_player
                board.last_move = (r, c)
                board.move_count += 1
                
                score = self.minimax(board, depth - 1, True)
                best_score = min(best_score, score)
                
                board.grid[r][c] = Board.EMPTY
                board.move_count -= 1
            return best_score
