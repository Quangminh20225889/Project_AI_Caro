from typing import List, Tuple, Set # Nhập các kiểu dữ liệu để gợi ý code (Type hinting)

class Board:
    # --- HÀM KHỞI TẠO BÀN CỜ ---
    # size: kích thước bàn cờ (ví dụ 15 là bàn cờ 15x15)
    # grid: ma trận lưu trạng thái bàn cờ hiện tại (tùy chọn)
    def __init__(self, size: int, grid: List[List[int]] = None):
        self.size = size # Lưu lại kích thước bàn cờ
        
        # Ý NGHĨA CÁC CON SỐ TRONG MA TRẬN:
        # 0: Ô trống (chưa ai đánh)
        # 1: Quân của AI (thường là X)
        # 2: Quân của Người chơi (thường là O)
        if grid:
            self.grid = grid # Nếu có sẵn trạng thái thì dùng luôn (thường dùng khi đệ quy Minimax copy bàn cờ)
        else:
            # Nếu chưa có, tạo ra một ma trận vuông toàn số 0 (bàn cờ mới hoàn toàn)
            # Dùng list comprehension để tạo mảng 2 chiều kích thước size x size
            self.grid = [[0 for _ in range(size)] for _ in range(size)]

    # --- HÀM LẤY DANH SÁCH CÁC NƯỚC ĐI HỢP LỆ ---
    # CỰC KỲ QUAN TRỌNG ĐỂ TỐI ƯU TỐC ĐỘ CHO AI
    def get_valid_moves(self) -> List[Tuple[int, int]]:
        """
        Tại sao không trả về toàn bộ ô trống?
        Nếu bàn cờ 15x15 có 225 ô, Minimax sẽ phải duyệt 225 nhánh ở ngay bước đầu tiên -> Máy tính bị treo ngay!
        Cách tối ưu: Ta chỉ cho AI đánh vào những ô trống xung quanh các ô đã có cờ (bán kính 2 ô).
        Bởi vì đánh ở một góc xa xăm trống trơn là nước đi hoàn toàn vô nghĩa.
        """
        moves = set() # Dùng kiểu Set để lưu tọa độ, tránh việc thêm trùng lặp cùng 1 ô
        has_piece = False # Cờ đánh dấu xem trên bàn cờ đã có quân nào chưa
        
        # Quét toàn bộ bàn cờ
        for r in range(self.size): # r là hàng (row)
            for c in range(self.size): # c là cột (column)
                # Nếu ô này có cờ (bất kể là của AI hay của Người)
                if self.grid[r][c] != 0:
                    has_piece = True
                    
                    # Quét một ô vuông kích thước 5x5 xung quanh quân cờ này (bán kính = 2)
                    for dr in range(-2, 3): # dr (delta row): chạy từ -2 đến 2
                        for dc in range(-2, 3): # dc (delta col): chạy từ -2 đến 2
                            # Bỏ qua ô trung tâm (chính là ô đang có cờ)
                            if dr == 0 and dc == 0:
                                continue
                                
                            # Tính tọa độ mới (nr, nc) của các ô xung quanh
                            nr, nc = r + dr, c + dc
                            
                            # Kiểm tra xem ô xung quanh này có nằm trong phạm vi bàn cờ không (không bị lọt ra ngoài rìa)
                            if 0 <= nr < self.size and 0 <= nc < self.size:
                                # Nếu ô này đang trống, thì đây là một nước đi có ý nghĩa (valid move)
                                if self.grid[nr][nc] == 0:
                                    moves.add((nr, nc)) # Thêm vào danh sách (vì dùng Set nên không sợ bị trùng)
        
        # Xử lý trường hợp đặc biệt: Bàn cờ hoàn toàn trống (Nước đi đầu tiên của ván game)
        if not has_piece:
            # AI sẽ mặc định đánh thẳng vào chính giữa bàn cờ (ví dụ 15//2 = 7 -> ô (7,7))
            return [(self.size // 2, self.size // 2)]
            
        return list(moves) # Chuyển Set thành List (mảng) và trả về

    # --- HÀM KIỂM TRA ĐIỀU KIỆN THẮNG ---
    # Truyền vào player (1 hoặc 2) để xem người đó đã thắng chưa
    def check_win(self, player: int) -> bool:
        """Check if the given player has won (5 in a row)."""
        # 4 hướng cần kiểm tra để tìm 5 quân liên tiếp:
        # (0, 1): Ngang (cùng hàng, tăng cột)
        # (1, 0): Dọc (tăng hàng, cùng cột)
        # (1, 1): Chéo xuôi (tăng hàng, tăng cột)
        # (1, -1): Chéo ngược (tăng hàng, giảm cột)
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        
        # Quét từng ô trên bàn cờ
        for r in range(self.size):
            for c in range(self.size):
                # Chỉ bắt đầu đếm nếu ô này là cờ của người chơi đang cần xét (player)
                if self.grid[r][c] != player:
                    continue
                
                # Tại ô này, rẽ nhánh quét theo 4 hướng đã định nghĩa ở trên
                for dr, dc in directions:
                    count = 1 # Đã có sẵn 1 quân tại ô (r, c) đang đứng
                    
                    # Đi tới 4 bước tiếp theo theo hướng (dr, dc)
                    for step in range(1, 5):
                        # Tính tọa độ ô tiếp theo
                        nr, nc = r + dr * step, c + dc * step
                        
                        # Nếu ô tiếp theo vẫn nằm trên bàn cờ VÀ là cờ của đúng người chơi đó
                        if 0 <= nr < self.size and 0 <= nc < self.size and self.grid[nr][nc] == player:
                            count += 1 # Đếm thêm 1
                        else:
                            # Đứt mạch (bị chặn hoặc hết ô), dừng kiểm tra hướng này luôn
                            break
                            
                    # Nếu đếm đủ 5 quân liên tiếp -> Thắng! Trả về True ngay lập tức
                    if count >= 5:
                        return True
                        
        # Quét hết bàn cờ mà không thấy -> Chưa thắng
        return False

    # --- HÀM KIỂM TRA BÀN CỜ ĐẦY ---
    # Dùng để xác định trường hợp Hòa (Draw)
    def is_full(self) -> bool:
        for r in range(self.size):
            for c in range(self.size):
                # Chỉ cần tìm thấy 1 ô trống (0) thì chứng tỏ bàn cờ chưa đầy
                if self.grid[r][c] == 0:
                    return False
        return True # Quét hết mà không thấy ô 0 nào -> Đầy

    # --- HÀM THỰC HIỆN NƯỚC ĐI ---
    # Đặt quân cờ của 'player' vào ô tọa độ (r, c)
    def make_move(self, r: int, c: int, player: int):
        self.grid[r][c] = player

    # --- HÀM THU HỒI NƯỚC ĐI (UNDO) ---
    # Xóa quân cờ tại ô (r, c) đưa về trạng thái trống (0). 
    # Hàm này cực kỳ quan trọng, được dùng liên tục trong thuật toán Minimax để quay lui (Backtracking)
    def undo_move(self, r: int, c: int):
        self.grid[r][c] = 0
