import random

class Board:
    EMPTY = '.'
    PLAYER_X = 'X' # Người chơi
    PLAYER_O = 'O' # Máy

    _zobrist_table = None
    _zobrist_turn_key = None

    @classmethod
    def _init_zobrist(cls, size):
        if cls._zobrist_table is None or len(cls._zobrist_table) != size:
            rng = random.Random(2026)
            # 0 for X, 1 for O
            cls._zobrist_table = [[[rng.getrandbits(64), rng.getrandbits(64)] for _ in range(size)] for _ in range(size)]
            cls._zobrist_turn_key = rng.getrandbits(64)

    def __init__(self, size=9):
        self.size = size
        self.grid = [[self.EMPTY for _ in range(size)] for _ in range(size)]
        self.last_move = None
        self.move_count = 0
        self._init_zobrist(size)
        self.current_hash = 0

    def copy(self):
        new_board = Board(self.size)
        new_board.grid = [row[:] for row in self.grid]
        new_board.last_move = self.last_move
        new_board.move_count = self.move_count
        new_board.current_hash = self.current_hash
        return new_board

    def _xor_hash(self, row, col, player):
        piece_idx = 0 if player == self.PLAYER_X else 1
        self.current_hash ^= self._zobrist_table[row][col][piece_idx]

    def make_move(self, row, col, player):
        if self.is_valid_move(row, col):
            self.grid[row][col] = player
            self.last_move = (row, col)
            self.move_count += 1
            self._xor_hash(row, col, player)
            self.current_hash ^= self._zobrist_turn_key
            return True
        return False

    def undo_move(self, row, col):
        player = self.grid[row][col]
        if player != self.EMPTY:
            self.grid[row][col] = self.EMPTY
            self.move_count -= 1
            self._xor_hash(row, col, player)
            self.current_hash ^= self._zobrist_turn_key
            if self.move_count == 0:
                self.last_move = None

    def is_valid_move(self, row, col):
        return 0 <= row < self.size and 0 <= col < self.size and self.grid[row][col] == self.EMPTY

    def get_valid_moves(self):
        """
        Trả về danh sách các nước đi có thể, ưu tiên các ô gần quân cờ có sẵn nhất.
        Sắp xếp các nước đi tốt giúp thuật toán Alpha-Beta cắt nhánh (pruning) cực kỳ hiệu quả.
        """
        if self.move_count == 0:
            return [(self.size // 2, self.size // 2)] # Bắt đầu ở giữa
        
        move_scores = {}
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] != self.EMPTY:
                    # Xem xét các ô trống xung quanh bán kính 2
                    for dr in [-2, -1, 0, 1, 2]:
                        for dc in [-2, -1, 0, 1, 2]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = r + dr, c + dc
                            if self.is_valid_move(nr, nc):
                                # Điểm càng cao nếu càng gần (bán kính 1 được 2 điểm, bán kính 2 được 1 điểm)
                                dist = max(abs(dr), abs(dc))
                                points = 2 if dist == 1 else 1
                                if (nr, nc) in move_scores:
                                    move_scores[(nr, nc)] += points
                                else:
                                    move_scores[(nr, nc)] = points
        
        # Sắp xếp các tọa độ theo điểm giảm dần
        sorted_moves = sorted(move_scores.keys(), key=lambda k: move_scores[k], reverse=True)
        return sorted_moves

    def check_win(self, player):
        """Kiểm tra điều kiện thắng: 4 quân liên tiếp không cần chặn 2 đầu."""
        if not self.last_move:
            return False
        
        # Để nhanh hơn, thay vì quét toàn bàn, ta chỉ cần quét quanh nước đi cuối cùng
        # (hoặc quét toàn bộ nếu muốn hàm check_win độc lập với last_move)
        # Tuy nhiên ta cứ quét toàn bộ cho chắc chắn.
        
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] == player:
                    # Ngang
                    if c + 3 < self.size and all(self.grid[r][c+i] == player for i in range(4)):
                        return [(r, c+i) for i in range(4)]
                    # Dọc
                    if r + 3 < self.size and all(self.grid[r+i][c] == player for i in range(4)):
                        return [(r+i, c) for i in range(4)]
                    # Chéo chính
                    if r + 3 < self.size and c + 3 < self.size and all(self.grid[r+i][c+i] == player for i in range(4)):
                        return [(r+i, c+i) for i in range(4)]
                    # Chéo phụ
                    if r + 3 < self.size and c - 3 >= 0 and all(self.grid[r+i][c-i] == player for i in range(4)):
                        return [(r+i, c-i) for i in range(4)]
        return False

    def is_full(self):
        return self.move_count >= self.size * self.size

    def is_terminal(self):
        return self.check_win(self.PLAYER_X) or self.check_win(self.PLAYER_O) or self.is_full()

    def print_board(self):
        print("  " + " ".join(str(i) for i in range(self.size)))
        for r in range(self.size):
            print(str(r) + " " + " ".join(self.grid[r]))
