from core.board import Board
from ai.minimax import MinimaxAI
from models.schemas import MoveResponse
import time
import random

class AIAgent:
    def __init__(self, difficulty: str):
        self.difficulty = difficulty
        if difficulty == "easy":
            self.depth = 1
        elif difficulty == "medium":
            self.depth = 2
        else:
            self.depth = 3 # Hard. Could be 4, but let's keep it responsive in Python

    def play(self, board: Board, ai_player: int) -> MoveResponse:
        minimax = MinimaxAI(self.depth)
        
        # Easy mode randomness: 30% chance to just pick a random valid move instead of the best move
        if self.difficulty == "easy" and random.random() < 0.3:
            start = time.time()
            valid_moves = board.get_valid_moves()
            move = random.choice(valid_moves) if valid_moves else None
            return MoveResponse(
                row=move[0] if move else -1,
                col=move[1] if move else -1,
                evaluation_time=time.time() - start,
                nodes_evaluated=1,
                heuristic_score=0,
                reason="Random move (Easy mode)"
            )
            
        best_move, eval_time, nodes, score = minimax.get_best_move(board, ai_player)
        
        reason = "Evaluated best move"
        if score > 10000:
            reason = "Found winning or forced block pattern"
        elif score < -10000:
            reason = "Defending against critical threat"
            
        return MoveResponse(
            row=best_move[0] if best_move else -1,
            col=best_move[1] if best_move else -1,
            evaluation_time=eval_time,
            nodes_evaluated=nodes,
            heuristic_score=int(score),
            reason=reason
        )
