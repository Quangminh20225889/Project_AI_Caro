from pydantic import BaseModel
from typing import List

class MoveRequest(BaseModel):
    board: List[List[int]]
    player: int
    difficulty: str
    size: int

class MoveResponse(BaseModel):
    row: int
    col: int
    evaluation_time: float
    nodes_evaluated: int
    heuristic_score: int
    reason: str

class MatchHistoryItem(BaseModel):
    mode: str
    difficulty: str
    board_size: int
    winner: int
    moves: int
