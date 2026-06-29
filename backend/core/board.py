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
            self.grid = grid 
        else:
            self.grid = [[0 for _ in range(size)] for _ in range(size)]

    # BẢN BACKUP: CODE CŨ (CHƯA CÓ MOVE ORDERING)
    # Tốc độ chậm hơn vì dùng Set (không phân loại ưu tiên vị trí giao tranh)
    # def get_valid_moves_old(self) -> List[Tuple[int, int]]:
    #     moves = set() # Dùng kiểu Set để lưu tọa độ, tránh việc thêm trùng lặp cùng 1 ô
    #     has_piece = False # Cờ đánh dấu xem trên bàn cờ đã có quân nào chưa
    #     
    #     for r in range(self.size): # r là hàng (row)
    #         for c in range(self.size): # c là cột (column)
    #             if self.grid[r][c] != 0:
    #                 has_piece = True
    #                 
    #                 # Quét một ô vuông kích thước 5x5 xung quanh quân cờ này (bán kính = 2)
    #                 for dr in range(-2, 3):
    #                     for dc in range(-2, 3):
    #                         if dr == 0 and dc == 0:
    #                             continue
    #                             
    #                         nr, nc = r + dr, c + dc
    #                         if 0 <= nr < self.size and 0 <= nc < self.size:
    #                             if self.grid[nr][nc] == 0:
    #                                 moves.add((nr, nc))
    #     
    #     if not has_piece:
    #         return [(self.size // 2, self.size // 2)]
    #         
    #     return list(moves) # Chuyển Set thành List (mảng) và trả về

    # --- HÀM LẤY DANH SÁCH CÁC NƯỚC ĐI HỢP LỆ (TỐI ƯU MOVE ORDERING) ---
    def get_valid_moves(self) -> List[Tuple[int, int]]:
        """
        Lấy các ô trống trong bán kính 2 ô xung quanh các quân cờ đã có.
        TỐI ƯU MOVE ORDERING: Sắp xếp các ô trống theo độ "nóng" (số lượng quân cờ xung quanh) 
        để giúp Alpha-Beta Pruning cắt nhánh nhanh gấp hàng chục lần.
        """
        moves_scores = {} # Dictionary lưu tọa độ ô trống và điểm ưu tiên của nó
        has_piece = False 
        
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] != 0:
                    has_piece = True
                    for dr in range(-2, 3): 
                        for dc in range(-2, 3): 
                            if dr == 0 and dc == 0:
                                continue
                                
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < self.size and 0 <= nc < self.size:
                                if self.grid[nr][nc] == 0:
                                    # CHẤM ĐIỂM ƯU TIÊN SẮP XẾP (MOVE ORDERING):
                                    # Nếu ô trống nằm sát quân cờ (bán kính 1) -> Ưu tiên cao (+2 điểm)
                                    # Nếu ô trống nằm cách 2 ô (bán kính 2) -> Ưu tiên thấp hơn (+1 điểm)
                                    # Ô nào lân cận càng nhiều quân cờ thì điểm cộng dồn càng lớn!
                                    weight = 2 if abs(dr) <= 1 and abs(dc) <= 1 else 1
                                    
                                    if (nr, nc) in moves_scores:
                                        moves_scores[(nr, nc)] += weight
                                    else:
                                        moves_scores[(nr, nc)] = weight
        
        if not has_piece:
            return [(self.size // 2, self.size // 2)]
            
        # Sắp xếp danh sách giảm dần theo điểm ưu tiên để Alpha-Beta xét nước đi "nóng" nhất trước
        sorted_moves = sorted(moves_scores.keys(), key=lambda k: moves_scores[k], reverse=True)
        return sorted_moves

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
