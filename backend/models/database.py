import sqlite3
from pathlib import Path
from typing import List, Dict

DB_PATH = Path(__file__).resolve().parents[1] / "match_history.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS matches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mode TEXT,
            difficulty TEXT,
            board_size INTEGER,
            winner INTEGER,
            moves INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def add_match(mode: str, difficulty: str, board_size: int, winner: int, moves: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO matches (mode, difficulty, board_size, winner, moves) VALUES (?, ?, ?, ?, ?)",
        (mode, difficulty, board_size, winner, moves)
    )
    conn.commit()
    conn.close()

def get_matches() -> List[Dict]:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM matches ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]
