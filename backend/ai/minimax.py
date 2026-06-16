from core.board import Board # Gọi class Board để tương tác với bàn cờ (make_move, undo_move)
from ai.heuristics import evaluate_board, WIN_SCORE # Nhập hàm chấm điểm và hằng số điểm Thắng
from typing import Tuple, Optional # Dùng để gợi ý kiểu dữ liệu (Type hinting)
import time # Dùng tính thời gian chạy thuật toán

class MinimaxAI:
    # Hàm khởi tạo, nhận vào độ sâu tối đa (max_depth) do Agent quy định
    def __init__(self, depth: int):
        self.max_depth = depth # Độ sâu tối đa được phép duyệt
        self.nodes_evaluated = 0 # Biến đếm xem AI đã "tưởng tượng" bao nhiêu bàn cờ trong đầu

    # HÀM GỐC: Nơi bắt đầu tìm kiếm nước đi
    def get_best_move(self, board: Board, player: int) -> Tuple[Optional[Tuple[int, int]], float, int, int]:
        """Hàm khởi tạo thuật toán: Thử đi từng ô trống và gọi đệ quy minimax để tìm nước đi tốt nhất"""
        start_time = time.time() # Bắt đầu đếm giờ
        self.nodes_evaluated = 0 # Reset bộ đếm số lượng node
        
        # Khởi tạo điểm tốt nhất ban đầu là âm vô cực (để bất kỳ điểm nào cũng lớn hơn nó)
        best_score = -float('inf') 
        best_move = None # Nước đi tốt nhất ban đầu là chưa có
        
        valid_moves = board.get_valid_moves() # Lấy danh sách toàn bộ các ô còn trống trên bàn cờ
        if not valid_moves:
            return None, 0.0, 0, 0 # Nếu bàn cờ đã đầy (Hòa), thoát luôn
            
        # VÒNG LẶP CHÍNH: Thử nghiệm từng nước đi có thể có
        for move in valid_moves:
            # 1. THỬ ĐÁNH: Đặt quân cờ của AI vào ô trống hiện tại (Sinh ra trạng thái tương lai)
            board.make_move(move[0], move[1], player)
            
            # 2. GỌI ĐỆ QUY MINIMAX: Bắt đầu dò sâu xuống nhánh này.
            # self.max_depth - 1: Độ sâu giảm dần.
            # alpha = -inf, beta = +inf: Khoảng giá trị cắt tỉa ban đầu
            # is_maximizing = False: Vì nước tiếp theo sẽ là lượt của Người chơi (Họ muốn điểm AI thấp nhất -> MIN)
            score = self.minimax(board, self.max_depth - 1, -float('inf'), float('inf'), False, player)
            
            # 3. RÚT QUÂN CỜ (Backtracking): Trả lại ô trống như cũ để vòng lặp thử tiếp ô khác
            board.undo_move(move[0], move[1])
            
            # 4. CẬP NHẬT KẾT QUẢ: Nếu ô vừa thử đem lại điểm cao hơn điểm tốt nhất đang giữ
            if score > best_score:
                best_score = score # Cập nhật mức điểm kỷ lục mới
                best_move = move # Lưu lại tọa độ nước đi này
                
            # ĐIỀU KIỆN TỐI ƯU SỚM: Nếu phát hiện nước đi mang lại chiến thắng (điểm >= WIN_SCORE / 2)
            # Dừng vòng lặp ngay lập tức vì không cần tìm nước nào tốt hơn nữa (Thắng là tốt nhất rồi)
            if best_score >= WIN_SCORE / 2:
                break
                
        eval_time = time.time() - start_time # Chốt thời gian chạy
        return best_move, eval_time, self.nodes_evaluated, best_score # Trả về kết quả cho Agent

    # HÀM ĐỆ QUY CỐT LÕI: Tự gọi lại chính nó để tạo thành cây trò chơi (Game Tree)
    def minimax(self, board: Board, depth: int, alpha: float, beta: float, is_maximizing: bool, ai_player: int) -> float:
        self.nodes_evaluated += 1 # Đếm thêm 1 trạng thái bàn cờ đã được duyệt
        opponent = 3 - ai_player # Xác định đối thủ (Nếu AI là 1 thì Đối thủ là 2 và ngược lại)
        
        # --- ĐIỀU KIỆN DỪNG ĐỆ QUY (Đạt đến nút lá - Leaf node) ---
        # 1. Nếu trạng thái này làm AI thắng
        if board.check_win(ai_player):
            return WIN_SCORE + depth # Cộng thêm depth: Chiến thắng ở độ sâu càng ít (thắng càng nhanh) thì điểm càng cao
            
        # 2. Nếu trạng thái này làm Đối thủ thắng
        if board.check_win(opponent):
            return -WIN_SCORE - depth # Trừ đi depth: Thua ở độ sâu càng sâu (cố gắng cù nhầy càng lâu) thì điểm âm càng ít
            
        # 3. Nếu đã phân nhánh hết giới hạn (depth == 0) hoặc bàn cờ đã đầy (hòa)
        if depth == 0 or board.is_full():
            # Dừng lại và gọi hàm evaluate_board (ở file heuristics.py) để "ước lượng" xem ai đang lợi thế hơn
            return evaluate_board(board.grid, board.size, ai_player)
            
        valid_moves = board.get_valid_moves() # Lấy danh sách ô trống cho lớp (layer) hiện tại
        
        # --- LƯỢT CỦA AI (TÌM NÚT MAX) ---
        if is_maximizing:
            max_eval = -float('inf') # Khởi tạo điểm trần cho AI (âm vô cực)
            for move in valid_moves:
                board.make_move(move[0], move[1], ai_player) # Đóng vai AI đánh
                # Lượt tiếp theo sẽ là Đối thủ (False)
                eval = self.minimax(board, depth - 1, alpha, beta, False, ai_player)
                board.undo_move(move[0], move[1]) # Backtrack rút cờ
                
                max_eval = max(max_eval, eval) # Chọn nhánh mang lại điểm số lớn hơn
                alpha = max(alpha, eval) # Alpha: Lưu lại điểm số lớn nhất mà AI chắc chắn đạt được ở nhánh này
                
                # --- CẮT TỈA ALPHA-BETA (Alpha-Beta Pruning) ---
                # Giải thích: Nếu beta <= alpha, có nghĩa là ở một nhánh nào đó (do Đối thủ chọn trước đó), 
                # Đối thủ đã tìm được một nước đi ép AI nhận điểm thấp hơn (beta).
                # Suy ra Đối thủ sẽ KHÔNG BAO GIỜ ngu ngốc chọn nhánh này (vì nhánh này AI có điểm alpha cao hơn).
                # Nhánh này coi như vô dụng. Dừng vòng lặp (break) để cắt bỏ toàn bộ phần cây còn lại!
                if beta <= alpha:
                    break
            return max_eval
            
        # --- LƯỢT CỦA ĐỐI THỦ (TÌM NÚT MIN) ---
        else:
            min_eval = float('inf') # Khởi tạo điểm sàn cho Đối thủ (dương vô cực)
            for move in valid_moves:
                board.make_move(move[0], move[1], opponent) # Đóng vai Đối thủ đánh
                # Lượt tiếp theo sẽ là AI (True)
                eval = self.minimax(board, depth - 1, alpha, beta, True, ai_player)
                board.undo_move(move[0], move[1]) # Backtrack rút cờ
                
                min_eval = min(min_eval, eval) # Chọn nhánh ép AI nhận điểm thấp hơn (tốt cho đối thủ)
                beta = min(beta, eval) # Beta: Lưu lại điểm số thấp nhất mà Đối thủ chắc chắn ép AI nhận được
                
                # CẮT TỈA TƯƠNG TỰ: Nếu AI phát hiện nhánh này tồi tệ hơn điểm alpha mà AI có thể đạt được ở nhánh khác,
                # AI sẽ KHÔNG BAO GIỜ đi vào nhánh này. Vô dụng, cắt nhánh luôn.
                if beta <= alpha:
                    break
            return min_eval
