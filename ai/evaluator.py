from core.board import Board

class Evaluator:
    @staticmethod
    def evaluate(board: Board, player: str) -> int:
        """
        Đánh giá điểm số của bảng hiện tại dưới góc nhìn của `player`.
        Giả sử `player` là người đang muốn tối đa hóa điểm.
        """
        opponent = Board.PLAYER_X if player == Board.PLAYER_O else Board.PLAYER_O
        score = 0
        
        # Hàm con đánh giá 1 chuỗi 4 ô
        def evaluate_window(window, player, opponent):
            score = 0
            player_count = window.count(player)
            empty_count = window.count(Board.EMPTY)
            opponent_count = window.count(opponent)

            if player_count == 4:
                score += 100000
            elif player_count == 3 and empty_count == 1:
                score += 1000
            elif player_count == 2 and empty_count == 2:
                score += 100
            elif player_count == 1 and empty_count == 3:
                score += 10

            if opponent_count == 4:
                score -= 100000
            elif opponent_count == 3 and empty_count == 1:
                score -= 1000
            elif opponent_count == 2 and empty_count == 2:
                score -= 100
            elif opponent_count == 1 and empty_count == 3:
                score -= 10
                
            return score

        size = board.size
        # Quét theo hàng ngang
        for r in range(size):
            for c in range(size - 3):
                window = [board.grid[r][c+i] for i in range(4)]
                score += evaluate_window(window, player, opponent)

        # Quét theo hàng dọc
        for r in range(size - 3):
            for c in range(size):
                window = [board.grid[r+i][c] for i in range(4)]
                score += evaluate_window(window, player, opponent)

        # Quét theo đường chéo chính (trái trên xuống phải dưới)
        for r in range(size - 3):
            for c in range(size - 3):
                window = [board.grid[r+i][c+i] for i in range(4)]
                score += evaluate_window(window, player, opponent)

        # Quét theo đường chéo phụ (phải trên xuống trái dưới)
        for r in range(size - 3):
            for c in range(3, size):
                window = [board.grid[r+i][c-i] for i in range(4)]
                score += evaluate_window(window, player, opponent)

        return score
