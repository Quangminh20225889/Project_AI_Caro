from core.board import Board
from ai.heuristics import evaluate_board, WIN_SCORE
from typing import Tuple, Optional
import time

class MinimaxAI:
    def __init__(self, depth: int):
        self.max_depth = depth
        self.nodes_evaluated = 0

    def get_best_move(self, board: Board, player: int) -> Tuple[Optional[Tuple[int, int]], float, int, int]:
        """Returns (best_move, evaluation_time, nodes_evaluated, heuristic_score)"""
        start_time = time.time()
        self.nodes_evaluated = 0
        
        best_score = -float('inf')
        best_move = None
        
        valid_moves = board.get_valid_moves()
        if not valid_moves:
            return None, 0.0, 0, 0
            
        # Optional: Order moves to improve alpha-beta pruning (e.g. by evaluating them simply first)
        
        for move in valid_moves:
            board.make_move(move[0], move[1], player)
            score = self.minimax(board, self.max_depth - 1, -float('inf'), float('inf'), False, player)
            board.undo_move(move[0], move[1])
            
            if score > best_score:
                best_score = score
                best_move = move
                
            # If we found a winning move, return immediately
            if best_score >= WIN_SCORE / 2:
                break
                
        eval_time = time.time() - start_time
        return best_move, eval_time, self.nodes_evaluated, best_score

    def minimax(self, board: Board, depth: int, alpha: float, beta: float, is_maximizing: bool, ai_player: int) -> float:
        self.nodes_evaluated += 1
        
        opponent = 3 - ai_player
        
        if board.check_win(ai_player):
            return WIN_SCORE + depth # Prefer faster wins
        if board.check_win(opponent):
            return -WIN_SCORE - depth # Prefer slower losses
            
        if depth == 0 or board.is_full():
            return evaluate_board(board.grid, board.size, ai_player)
            
        valid_moves = board.get_valid_moves()
        
        if is_maximizing:
            max_eval = -float('inf')
            for move in valid_moves:
                board.make_move(move[0], move[1], ai_player)
                eval = self.minimax(board, depth - 1, alpha, beta, False, ai_player)
                board.undo_move(move[0], move[1])
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in valid_moves:
                board.make_move(move[0], move[1], opponent)
                eval = self.minimax(board, depth - 1, alpha, beta, True, ai_player)
                board.undo_move(move[0], move[1])
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval
