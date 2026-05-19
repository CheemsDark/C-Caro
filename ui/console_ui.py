from core.game_engine import GameEngine
import os

class ConsoleUI:
    def __init__(self):
        pass
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def draw_board(self, board):
        print("\n--- BÀN CỜ CARO (4 quân liên tiếp thắng) ---")
        # In tiêu đề cột
        header = "   " + " ".join(f"{i:2}" for i in range(board.size))
        print(header)
        
        for r in range(board.size):
            row_str = f"{r:2} "
            for c in range(board.size):
                cell = board.grid[r][c]
                if cell == board.PLAYER_X:
                    row_str += " \033[91mX\033[0m " # X màu đỏ
                elif cell == board.PLAYER_O:
                    row_str += " \033[94mO\033[0m " # O màu xanh
                else:
                    row_str += " . "
            print(row_str)
        print()

    def play(self, engine: GameEngine):
        while engine.status == "ongoing":
            self.clear_screen()
            self.draw_board(engine.board)
            
            if engine.current_player == engine.board.PLAYER_X:
                print("Lượt của Người chơi (X).")
                try:
                    move_str = input("Nhập tọa độ hàng và cột cách nhau bởi dấu cách (VD: 4 5): ")
                    parts = move_str.strip().split()
                    if len(parts) != 2:
                        raise ValueError
                    r, c = map(int, parts)
                    if not engine.make_human_move(r, c):
                        print("Nước đi không hợp lệ! Ô đã có quân cờ hoặc nằm ngoài bàn cờ.")
                        input("Nhấn Enter để thử lại...")
                except ValueError:
                    print("Định dạng không hợp lệ. Vui lòng nhập đúng 2 số nguyên.")
                    input("Nhấn Enter để thử lại...")
            else:
                print("Máy đang suy nghĩ...")
                result = engine.make_ai_move()
                print(f"\n=> Máy (O) đã đánh tại: {result['move']}")
                print(f"[AI Stats] Thuật toán: {engine.ai.algorithm.upper()} | Depth: {engine.ai.depth}")
                print(f"[AI Stats] Điểm đánh giá (Heuristic): {result['score']}")
                print(f"[AI Stats] Số trạng thái đã duyệt: {result['nodes']} nodes")
                print(f"[AI Stats] Thời gian chạy: {result['time_ms']:.2f} ms")
                input("\nNhấn Enter để tiếp tục...")
                
        self.clear_screen()
        self.draw_board(engine.board)
        if engine.status == "x_won":
            print("===========================")
            print("  CHÚC MỪNG! Bạn đã thắng! ")
            print("===========================")
        elif engine.status == "o_won":
            print("===========================")
            print("  RẤT TIẾC! Máy đã thắng!  ")
            print("===========================")
        else:
            print("===========================")
            print("    HÒA! Bàn cờ đã kín.    ")
            print("===========================")

    def play_ai_vs_ai(self, engine: GameEngine, ai_x_algo: str, ai_x_depth: int, ai_o_algo: str, ai_o_depth: int):
        from ai.agent import AIAgent
        import time
        agent_x = AIAgent(algorithm=ai_x_algo, depth=ai_x_depth, ai_player=engine.board.PLAYER_X, human_player=engine.board.PLAYER_O)
        agent_o = AIAgent(algorithm=ai_o_algo, depth=ai_o_depth, ai_player=engine.board.PLAYER_O, human_player=engine.board.PLAYER_X)
        
        while engine.status == "ongoing":
            self.clear_screen()
            self.draw_board(engine.board)
            
            if engine.current_player == engine.board.PLAYER_X:
                print("Máy X đang suy nghĩ...")
                result = agent_x.get_move(engine.board.copy())
                if result["move"]:
                    r, c = result["move"]
                    engine.board.make_move(r, c, engine.board.PLAYER_X)
                    engine._check_status()
                    if engine.status == "ongoing":
                        engine.current_player = engine.board.PLAYER_O
                print(f"\n=> Máy (X) đã đánh tại: {result['move']}")
                print(f"[AI Stats] Thuật toán: {ai_x_algo.upper()} | Depth: {ai_x_depth}")
            else:
                print("Máy O đang suy nghĩ...")
                result = agent_o.get_move(engine.board.copy())
                if result["move"]:
                    r, c = result["move"]
                    engine.board.make_move(r, c, engine.board.PLAYER_O)
                    engine._check_status()
                    if engine.status == "ongoing":
                        engine.current_player = engine.board.PLAYER_X
                print(f"\n=> Máy (O) đã đánh tại: {result['move']}")
                print(f"[AI Stats] Thuật toán: {ai_o_algo.upper()} | Depth: {ai_o_depth}")
                
            print(f"[AI Stats] Điểm đánh giá: {result['score']}")
            print(f"[AI Stats] Số nodes duyệt: {result['nodes']}")
            print(f"[AI Stats] Thời gian chạy: {result['time_ms']:.2f} ms")
            time.sleep(1.0)
            
        self.clear_screen()
        self.draw_board(engine.board)
        if engine.status == "x_won":
            print("===========================")
            print("  CHÚC MỪNG MÁY X THẮNG!   ")
            print("===========================")
        elif engine.status == "o_won":
            print("===========================")
            print("  CHÚC MỪNG MÁY O THẮNG!   ")
            print("===========================")
        else:
            print("===========================")
            print("    HÒA! Bàn cờ đã kín.    ")
            print("===========================")
