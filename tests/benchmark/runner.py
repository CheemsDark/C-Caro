import sys
import os
import csv
import time

sys.stdout.reconfigure(encoding='utf-8')

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from core.board import Board
from ai.agent import AIAgent

def setup_board(state_type):
    board = Board(size=9)
    if state_type == "early":
        board.make_move(4, 4, Board.PLAYER_X)
        board.make_move(4, 5, Board.PLAYER_O)
    elif state_type == "mid":
        moves = [(4,4,'X'), (4,5,'O'), (5,5,'X'), (3,4,'O'), (3,5,'X'), (5,4,'O'), (2,4,'X')]
        for r, c, p in moves:
            board.make_move(r, c, p)
    elif state_type == "ai_win":
        board.make_move(1, 1, 'X')
        board.make_move(2, 2, 'O')
        board.make_move(1, 2, 'X')
        board.make_move(3, 3, 'O')
        board.make_move(1, 3, 'X')
        board.make_move(4, 4, 'O')
    elif state_type == "human_win":
        board.make_move(2, 2, 'X')
        board.make_move(1, 1, 'O')
        board.make_move(3, 3, 'X')
        board.make_move(1, 2, 'O')
        board.make_move(4, 4, 'X')
    elif state_type == "complex":
        moves = [
            (4,4,'X'), (4,5,'O'), (5,5,'X'), (5,4,'O'), 
            (3,3,'X'), (6,6,'O'), (3,5,'X'), (5,3,'O'),
            (4,3,'X'), (4,6,'O'), (6,4,'X'), (2,4,'O')
        ]
        for r, c, p in moves:
            board.make_move(r, c, p)
    return board

def run_benchmark():
    states = ["early", "mid", "ai_win", "human_win", "complex"]
    depths = [1, 2, 3, 4]
    algorithms = ["minimax", "alpha_beta"]
    
    log_dir = os.path.join(os.path.dirname(__file__), "logs")
    os.makedirs(log_dir, exist_ok=True)
    csv_file = os.path.join(log_dir, "benchmark_results.csv")
    
    print("Bắt đầu chạy Benchmark...")
    print(f"Dữ liệu sẽ được lưu tại: {csv_file}")
    
    with open(csv_file, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["State", "Depth", "Algorithm", "Nodes", "Time_ms", "Score"])
        
        for state in states:
            board_template = setup_board(state)
            for depth in depths:
                for algo in algorithms:
                    board = board_template.copy()
                    
                    if algo == "minimax" and depth > 3:
                        continue
                        
                    agent = AIAgent(algorithm=algo, depth=depth)
                    print(f"Testing {algo} at depth {depth} on state {state}...")
                    
                    result = agent.get_move(board)
                    
                    writer.writerow([
                        state, 
                        depth, 
                        algo, 
                        result['nodes'], 
                        round(result['time_ms'], 2),
                        result['score']
                    ])
                    f.flush()
    
    print("Benchmark hoàn tất! Bạn có thể mở file analysis.ipynb để xem biểu đồ.")

if __name__ == "__main__":
    run_benchmark()
