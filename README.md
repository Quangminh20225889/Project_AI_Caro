<h1 style="color: #E91E63; font-weight: bold;">Dự án AI Caro</h1>

Game Caro/Gomoku với giao diện React và hệ thống xử lý FastAPI. Trí tuệ nhân tạo AI sử dụng thuật toán Minimax kết hợp cắt tỉa Alpha-Beta và đánh giá dựa trên các mẫu nước cờ.

<h2 style="color: #4CAF50; font-weight: bold;">Hướng dẫn chạy Backend (Hệ thống xử lý)</h2>

Mở màn hình dòng lệnh (Terminal/Command Prompt) và chạy lần lượt:

- <span style="color:#007ACC">cd backend</span> : Di chuyển vào thư mục backend
- <span style="color:#007ACC">python -m venv venv</span> : Tạo môi trường ảo
- <span style="color:#007ACC">venv\Scripts\activate</span> : Bật môi trường ảo (Mac/Linux dùng: <span style="color:#007ACC">source venv/bin/activate</span>)
- <span style="color:#007ACC">pip install -r requirements.txt</span> : Cài đặt các thư viện cần thiết
- <span style="color:#007ACC">uvicorn main:app --reload</span> : Chạy server (tại http://localhost:8000)

<h2 style="color: #2196F3; font-weight: bold;">Hướng dẫn chạy Frontend (Giao diện web)</h2>

Mở một màn hình dòng lệnh mới và chạy lần lượt:

- <span style="color:#007ACC">cd frontend</span> : Di chuyển vào thư mục frontend
- <span style="color:#007ACC">npm install</span> : Tải và cài đặt các công cụ cần thiết
- <span style="color:#007ACC">npm run dev</span> : Khởi chạy trang web (tại http://localhost:5173)

<h2 style="color: #9C27B0; font-weight: bold;">Cấu trúc thư mục chính</h2>

Phần backend:

- Thư mục <span style="color:#007ACC">ai</span> : Thuật toán Minimax và AI đánh cờ
- Thư mục <span style="color:#007ACC">api</span> : Các API kết nối với giao diện
- Thư mục <span style="color:#007ACC">core</span> : Luật chơi và logic bàn cờ
- Thư mục <span style="color:#007ACC">models</span> : Cấu trúc dữ liệu và lịch sử ván đấu

Phần frontend:

- Thư mục <span style="color:#007ACC">src</span> : Các trang giao diện React và kết nối API
