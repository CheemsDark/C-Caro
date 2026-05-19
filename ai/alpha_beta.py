from core.board import Board
from ai.evaluator import Evaluator
import math
import time
import json
import os

# Consts for TT
TT_EXACT = 0
TT_LOWERBOUND = 1
TT_UPPERBOUND = 2

class AlphaBetaAI:
    def __init__(self, ai_player=Board.PLAYER_O, human_player=Board.PLAYER_X):
        self.ai_player = ai_player
        self.human_player = human_player
        self.nodes_visited = 0
        self.transposition_table = {}
        
        self.time_limit = 5.0
        self.beam_width_root = 15
        self.beam_width_inner = 10
        self._load_config()

    def _load_config(self):
        config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config", "config.json")
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
                self.time_limit = config.get("time_limit", 5.0)
                self.beam_width_root = config.get("beam_width_root", 15)
                self.beam_width_inner = config.get("beam_width_inner", 10)
        except Exception as e:
            print(f"Không thể load config.json: {e}. Sử dụng mặc định.")

    def _line_metrics(self, board, r, c, piece, dr, dc):
        total = 1
        open_ends = 0
        size = board.size
        
        nr, nc = r + dr, c + dc
        while 0 <= nr < size and 0 <= nc < size and board.grid[nr][nc] == piece:
            total += 1
            nr += dr
            nc += dc
        if 0 <= nr < size and 0 <= nc < size and board.grid[nr][nc] == Board.EMPTY:
            open_ends += 1

        nr, nc = r - dr, c - dc
        while 0 <= nr < size and 0 <= nc < size and board.grid[nr][nc] == piece:
            total += 1
            nr -= dr
            nc -= dc
        if 0 <= nr < size and 0 <= nc < size and board.grid[nr][nc] == Board.EMPTY:
            open_ends += 1

        return total, open_ends

    def _local_pattern_score(self, board, r, c, piece):
        score = 0
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for dr, dc in directions:
            total, open_ends = self._line_metrics(board, r, c, piece, dr, dc)
            if total >= 5:
                score += 10000000
            elif total == 4 and open_ends == 2:
                score += 2000000
            elif total == 4 and open_ends == 1:
                score += 500000
            elif total == 3 and open_ends == 2:
                score += 100000
            elif total == 3 and open_ends == 1:
                score += 10000
            elif total == 2 and open_ends == 2:
                score += 1000
        return score

    def _quick_move_score(self, board, r, c):
        attack_score = self._local_pattern_score(board, r, c, self.ai_player)
        block_score = self._local_pattern_score(board, r, c, self.human_player)
        
        if attack_score >= 10000000:
            return 20000000
        if block_score >= 10000000:
            return 10000000 + 1
        return attack_score * 2 + block_score

    def _sort_moves(self, board, possible_moves, pv_move=None):
        import random
        # Trộn ngẫu nhiên danh sách nước đi trước khi chấm điểm để phá vỡ tính cố định
        shuffled_moves = list(possible_moves)
        random.shuffle(shuffled_moves)
        
        scored_moves = []
        for r, c in shuffled_moves:
            if pv_move and (r, c) == pv_move:
                scored_moves.append((float('inf'), (r, c)))
            else:
                # Thêm nhiễu ngẫu nhiên nhỏ (0-9) để rẽ nhánh ngẫu nhiên nếu các nước đi có cùng số điểm
                jitter = random.randint(0, 9)
                base_score = self._quick_move_score(board, r, c)
                scored_moves.append((base_score * 10 + jitter, (r, c)))
        
        scored_moves.sort(key=lambda item: item[0], reverse=True)
        return [move for _, move in scored_moves]

    def _find_tactical_forced_move(self, board, valid_moves):
        for r, c in valid_moves:
            if self._local_pattern_score(board, r, c, self.ai_player) >= 10000000:
                return (r, c)
        
        for r, c in valid_moves:
            if self._local_pattern_score(board, r, c, self.human_player) >= 10000000:
                return (r, c)
                
        for r, c in valid_moves:
            if self._local_pattern_score(board, r, c, self.ai_player) >= 2000000:
                return (r, c)
                
        for r, c in valid_moves:
            if self._local_pattern_score(board, r, c, self.human_player) >= 2000000:
                return (r, c)
                
        return None

    def get_best_move(self, board: Board, max_depth: int):
        self.nodes_visited = 0
        self.transposition_table.clear()
        start_time = time.time()
        deadline = start_time + self.time_limit
        
        best_move = None
        best_score = -math.inf
        pv_move = None

        valid_moves = board.get_valid_moves()
        if not valid_moves:
            return None, 0, 0, 0

        forced_move = self._find_tactical_forced_move(board, valid_moves)
        if forced_move:
            return forced_move, 20000000, 0, (time.time() - start_time) * 1000

        for depth in range(1, max_depth + 1):
            if time.time() >= deadline and depth > 1:
                break
                
            current_best_score = -math.inf
            current_best_move = None
            alpha = -math.inf
            beta = math.inf
            
            ordered_moves = self._sort_moves(board, valid_moves, pv_move)
            if len(ordered_moves) > self.beam_width_root:
                ordered_moves = ordered_moves[:self.beam_width_root]
            
            completed = True
            for r, c in ordered_moves:
                if time.time() >= deadline and depth > 1:
                    completed = False
                    break
                    
                board.make_move(r, c, self.ai_player)
                score = self.alphabeta(board, depth - 1, alpha, beta, False, deadline)
                board.undo_move(r, c)
                
                if score > current_best_score:
                    current_best_score = score
                    current_best_move = (r, c)
                    
                alpha = max(alpha, current_best_score)
            
            if completed and current_best_move:
                best_move = current_best_move
                best_score = current_best_score
                pv_move = current_best_move
            elif not completed:
                break
                
        if best_move is None:
            best_move = self._sort_moves(board, valid_moves)[0]
            
        execution_time = (time.time() - start_time) * 1000
        return best_move, best_score, self.nodes_visited, execution_time

    def alphabeta(self, board: Board, depth: int, alpha: float, beta: float, is_maximizing: bool, deadline: float):
        if time.time() >= deadline:
            return Evaluator.evaluate(board, self.ai_player)

        self.nodes_visited += 1
        
        hash_key = board.current_hash
        tt_entry = self.transposition_table.get(hash_key)
        
        if tt_entry and tt_entry['depth'] >= depth:
            if tt_entry['flag'] == TT_EXACT:
                return tt_entry['score']
            elif tt_entry['flag'] == TT_LOWERBOUND:
                alpha = max(alpha, tt_entry['score'])
            elif tt_entry['flag'] == TT_UPPERBOUND:
                beta = min(beta, tt_entry['score'])
                
            if alpha >= beta:
                return tt_entry['score']

        if board.check_win(self.ai_player):
            return 1000000 + depth
        if board.check_win(self.human_player):
            return -1000000 - depth
        if board.is_full() or depth == 0:
            return Evaluator.evaluate(board, self.ai_player)

        valid_moves = board.get_valid_moves()
        pv_move = tt_entry['best_move'] if tt_entry else None
        ordered_moves = self._sort_moves(board, valid_moves, pv_move)
        
        if len(ordered_moves) > self.beam_width_inner:
            ordered_moves = ordered_moves[:self.beam_width_inner]

        original_alpha = alpha
        best_move = None
        
        if is_maximizing:
            best_score = -math.inf
            for r, c in ordered_moves:
                board.make_move(r, c, self.ai_player)
                score = self.alphabeta(board, depth - 1, alpha, beta, False, deadline)
                board.undo_move(r, c)
                
                if score > best_score:
                    best_score = score
                    best_move = (r, c)
                
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
        else:
            best_score = math.inf
            for r, c in ordered_moves:
                board.make_move(r, c, self.human_player)
                score = self.alphabeta(board, depth - 1, alpha, beta, True, deadline)
                board.undo_move(r, c)
                
                if score < best_score:
                    best_score = score
                    best_move = (r, c)
                    
                beta = min(beta, best_score)
                if beta <= alpha:
                    break

        flag = TT_EXACT
        if best_score <= original_alpha:
            flag = TT_UPPERBOUND
        elif best_score >= beta:
            flag = TT_LOWERBOUND
            
        self.transposition_table[hash_key] = {
            'depth': depth,
            'score': best_score,
            'flag': flag,
            'best_move': best_move
        }

        return best_score
