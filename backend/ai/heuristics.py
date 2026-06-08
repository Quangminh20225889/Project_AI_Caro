from typing import List

# Constants for evaluation
WIN_SCORE = 10000000
OPEN_FOUR = 100000
BLOCKED_FOUR = 10000
OPEN_THREE = 10000
BLOCKED_THREE = 1000
OPEN_TWO = 100
BLOCKED_TWO = 10

def evaluate_line(line: List[int], player: int, opponent: int) -> int:
    """Evaluate a single line of length 5 to 9."""
    # This is a simplified pattern matcher for a continuous line.
    score = 0
    line_str = "".join(str(x) for x in line)
    
    p = str(player)
    o = str(opponent)
    e = "0"
    
    # Patterns for player
    p_win = p * 5
    p_open_4 = e + p * 4 + e
    p_blocked_4_1 = o + p * 4 + e
    p_blocked_4_2 = e + p * 4 + o
    p_open_3 = e + p * 3 + e
    p_blocked_3_1 = o + p * 3 + e + e
    p_blocked_3_2 = e + e + p * 3 + o
    p_open_2 = e + e + p * 2 + e + e
    
    # Check Player patterns
    if p_win in line_str: return WIN_SCORE
    if p_open_4 in line_str: score += OPEN_FOUR
    if p_blocked_4_1 in line_str or p_blocked_4_2 in line_str: score += BLOCKED_FOUR
    if p_open_3 in line_str: score += OPEN_THREE
    if p_blocked_3_1 in line_str or p_blocked_3_2 in line_str: score += BLOCKED_THREE
    if p_open_2 in line_str: score += OPEN_TWO

    # We subtract opponent score from the perspective of the player to make it zero-sum-ish,
    # but typically it's evaluated for a single board state.
    # The opponent having an open 4 is very bad.
    o_win = o * 5
    o_open_4 = e + o * 4 + e
    o_blocked_4_1 = p + o * 4 + e
    o_blocked_4_2 = e + o * 4 + p
    o_open_3 = e + o * 3 + e
    
    if o_win in line_str: return -WIN_SCORE
    if o_open_4 in line_str: score -= OPEN_FOUR * 2  # Block immediately
    if o_blocked_4_1 in line_str or o_blocked_4_2 in line_str: score -= BLOCKED_FOUR
    if o_open_3 in line_str: score -= OPEN_THREE * 2

    return score

def evaluate_board(grid: List[List[int]], size: int, player: int) -> int:
    opponent = 3 - player
    total_score = 0
    
    # Horizontal
    for r in range(size):
        row = grid[r]
        total_score += evaluate_line(row, player, opponent)
        
    # Vertical
    for c in range(size):
        col = [grid[r][c] for r in range(size)]
        total_score += evaluate_line(col, player, opponent)
        
    # Diagonals (top-left to bottom-right)
    for d in range(-size + 1, size):
        diag = []
        for r in range(size):
            c = r - d
            if 0 <= c < size:
                diag.append(grid[r][c])
        if len(diag) >= 5:
            total_score += evaluate_line(diag, player, opponent)
            
    # Diagonals (top-right to bottom-left)
    for d in range(2 * size - 1):
        diag = []
        for r in range(size):
            c = d - r
            if 0 <= c < size:
                diag.append(grid[r][c])
        if len(diag) >= 5:
            total_score += evaluate_line(diag, player, opponent)
            
    return total_score
