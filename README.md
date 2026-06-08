# Project AI Caro

Game Caro/Gomoku với frontend React và backend FastAPI. AI sử dụng Minimax kết hợp Alpha-Beta pruning và heuristic theo các mẫu nước cờ.

## Chạy backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Backend chạy tại:

```text
http://localhost:8000
```

## Chạy frontend

Mở terminal khác:

```bash
cd frontend
npm install
npm run dev
```

Frontend thường chạy tại:

```text
http://localhost:5173
```

## Cấu trúc chính

```text
backend/
  ai/        Minimax, heuristic, AI agent
  api/       FastAPI endpoints
  core/      Board logic
  models/    Schema và SQLite history

frontend/
  src/       React pages, components, API service
```
