from typing import List, Tuple, Set

class Board:
    def __init__(self, size: int, grid: List[List[int]] = None):
        self.size = size
        # 0: empty, 1: player 1 (X), 2: player 2 (O)
        if grid:
            self.grid = grid
        else:
            self.grid = [[0 for _ in range(size)] for _ in range(size)]

    def get_valid_moves(self) -> List[Tuple[int, int]]:
        """
        To optimize, only return empty cells that are adjacent (within distance 2)
        to an already placed piece. If board is empty, return center.
        """
        moves = set()
        has_piece = False
        
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] != 0:
                    has_piece = True
                    # Check distance 1 and 2
                    for dr in range(-2, 3):
                        for dc in range(-2, 3):
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < self.size and 0 <= nc < self.size:
                                if self.grid[nr][nc] == 0:
                                    moves.add((nr, nc))
        
        if not has_piece:
            return [(self.size // 2, self.size // 2)]
            
        return list(moves)

    def check_win(self, player: int) -> bool:
        """Check if the given player has won (5 in a row)."""
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] != player:
                    continue
                
                for dr, dc in directions:
                    count = 1
                    for step in range(1, 5):
                        nr, nc = r + dr * step, c + dc * step
                        if 0 <= nr < self.size and 0 <= nc < self.size and self.grid[nr][nc] == player:
                            count += 1
                        else:
                            break
                    if count >= 5:
                        return True
        return False

    def is_full(self) -> bool:
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] == 0:
                    return False
        return True

    def make_move(self, r: int, c: int, player: int):
        self.grid[r][c] = player

    def undo_move(self, r: int, c: int):
        self.grid[r][c] = 0
