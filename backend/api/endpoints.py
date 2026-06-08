from fastapi import APIRouter, HTTPException
from models.schemas import MoveRequest, MoveResponse, MatchHistoryItem
from ai.agent import AIAgent
from core.board import Board
from models.database import add_match, get_matches

router = APIRouter()

@router.post("/play", response_model=MoveResponse)
def play_move(request: MoveRequest):
    board = Board(request.size, request.board)
    agent = AIAgent(request.difficulty)
    
    if board.is_full():
        raise HTTPException(status_code=400, detail="Board is full")
        
    response = agent.play(board, request.player)
    return response

@router.post("/history")
def save_match(match: MatchHistoryItem):
    add_match(match.mode, match.difficulty, match.board_size, match.winner, match.moves)
    return {"status": "success"}

@router.get("/history")
def fetch_history():
    return get_matches()
