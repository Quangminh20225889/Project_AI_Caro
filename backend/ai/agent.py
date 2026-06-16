from core.board import Board # Gọi class Board để lấy trạng thái bàn cờ hiện tại
from ai.minimax import MinimaxAI # Gọi class MinimaxAI chứa thuật toán Minimax và Alpha-Beta
from models.schemas import MoveResponse # Định nghĩa kiểu dữ liệu trả về cho Frontend (tọa độ, thời gian, điểm)
import time # Dùng để tính toán thời gian AI suy nghĩ (evaluation_time)
import random # Dùng để tạo tính ngẫu nhiên (dành riêng cho chế độ Easy)

class AIAgent:
    # Hàm khởi tạo Agent, nhận vào mức độ khó do người dùng chọn (easy, medium, hard)
    def __init__(self, difficulty: str):
        # Lưu lại mức độ khó
        self.difficulty = difficulty
        
        # Thiết lập độ sâu (Depth limit) dựa trên độ khó.
        # Độ sâu càng lớn -> AI nhìn trước càng nhiều bước -> Càng thông minh nhưng tính toán càng lâu.
        if difficulty == "easy":
            self.depth = 1 # Dễ: Chỉ tính trước 1 bước (chỉ lo phòng thủ/tấn công ngay lập tức, không biết gài bẫy)
        elif difficulty == "medium":
            self.depth = 2 # Trung bình: Tính trước 2 bước
        else:
            self.depth = 3 # Khó: Tính trước 3 bước. Đây là mức tối ưu trong Python để game không bị lag (vẫn phản hồi < 2s).

    # Hàm play: Được gọi khi đến lượt AI đánh
    def play(self, board: Board, ai_player: int) -> MoveResponse:
        # Khởi tạo đối tượng thuật toán Minimax với độ sâu đã thiết lập ở trên
        minimax = MinimaxAI(self.depth)
        
        # --- XỬ LÝ RIÊNG CHO CHẾ ĐỘ DỄ (EASY MODE) ---
        # Ở chế độ dễ, AI có 30% tỷ lệ cố tình đánh "ngu" (chọn bừa 1 ô) thay vì đi nước tối ưu.
        # Điều này giúp tạo cảm giác chân thực như con người (có lúc bất cẩn), giúp người chơi mới có thể thắng.
        if self.difficulty == "easy" and random.random() < 0.3: # random.random() sinh số ngẫu nhiên từ 0.0 đến 1.0
            start = time.time() # Bắt đầu bấm giờ
            valid_moves = board.get_valid_moves() # Lấy danh sách tất cả các ô còn trống trên bàn cờ
            # Nếu còn ô trống thì chọn bốc thăm ngẫu nhiên 1 ô, nếu hết ô thì None
            move = random.choice(valid_moves) if valid_moves else None
            
            # Trả về kết quả ngay lập tức
            return MoveResponse(
                row=move[0] if move else -1, # Tọa độ hàng ngang
                col=move[1] if move else -1, # Tọa độ cột dọc
                evaluation_time=time.time() - start, # Thời gian xử lý gần như = 0
                nodes_evaluated=1, # Chỉ duyệt 1 trạng thái duy nhất
                heuristic_score=0, # Điểm đánh giá = 0 vì chọn ngẫu nhiên
                reason="Random move (Easy mode)" # Ghi chú lý do cho Frontend biết
            )
            
        # --- CHẾ ĐỘ TRUNG BÌNH & KHÓ (GỌI THUẬT TOÁN) ---
        # Gọi hàm get_best_move của thuật toán Minimax để tính toán nước đi tốt nhất.
        # Trả về 4 thông tin: Tọa độ tốt nhất, Thời gian suy nghĩ, Số lượng nhánh cây đã duyệt, Điểm số của nước đi.
        best_move, eval_time, nodes, score = minimax.get_best_move(board, ai_player)
        
        # Dựa vào điểm số để đưa ra "lời bình luận" (reason) cho nước đi đó
        reason = "Evaluated best move" # Mặc định là: "Đây là nước đi tốt nhất tính toán được"
        if score > 10000:
            # Nếu điểm > 10,000 tức là AI đã thấy đường thắng (5 quân hoặc 4 quân hở 2 đầu)
            reason = "Found winning or forced block pattern" 
        elif score < -10000:
            # Nếu điểm bị âm quá nặng, tức là AI phát hiện đối thủ sắp thắng, buộc phải chặn
            reason = "Defending against critical threat"
            
        # Đóng gói tất cả thông tin và trả về cho Frontend
        return MoveResponse(
            row=best_move[0] if best_move else -1, # Tọa độ hàng, nếu không có nước đi (bàn cờ đầy) thì trả về -1
            col=best_move[1] if best_move else -1, # Tọa độ cột
            evaluation_time=eval_time, # Tổng thời gian AI suy nghĩ
            nodes_evaluated=nodes, # Tổng số trạng thái bàn cờ AI đã mô phỏng trong đầu
            heuristic_score=int(score), # Điểm số của bàn cờ
            reason=reason # Lý do (để in ra màn hình hoặc debug)
        )
