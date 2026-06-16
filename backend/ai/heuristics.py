from typing import List # Import List để khai báo kiểu dữ liệu mảng

# --- HỆ THỐNG CHẤM ĐIỂM CÁC THẾ CỜ (CONSTANTS) ---
# Điểm số được thiết kế cách biệt nhau rất xa (10 triệu -> 100 ngàn -> 10 ngàn)
# Mục đích: Ép AI nhận thức được mức độ quan trọng. Ví dụ: AI thà bỏ 10 cái OPEN_THREE (1 vạn) để chặn 1 cái OPEN_FOUR (10 vạn) của đối thủ.
WIN_SCORE = 10000000   # 10,000,000 điểm: Chắc chắn thắng (Đạt 5 quân liên tiếp).
OPEN_FOUR = 100000     # 100,000 điểm: 4 quân hở 2 đầu (Ví dụ: Trống-Đen-Đen-Đen-Đen-Trống). Đối thủ không thể chặn kịp.
BLOCKED_FOUR = 10000   # 10,000 điểm: 4 quân bị chặn 1 đầu (Ví dụ: Trắng-Đen-Đen-Đen-Đen-Trống). Còn cơ hội ăn nếu đối thủ không chặn.
OPEN_THREE = 10000     # 10,000 điểm: 3 quân hở 2 đầu. Rất tiềm năng để phát triển thành OPEN_FOUR.
BLOCKED_THREE = 1000   # 1,000 điểm: 3 quân bị chặn 1 đầu.
OPEN_TWO = 100         # 100 điểm: 2 quân hở 2 đầu. Dùng để tích tiểu thành đại.
BLOCKED_TWO = 10       # 10 điểm: 2 quân bị chặn 1 đầu. Giá trị thấp nhất.

# Hàm đánh giá một "đường thẳng" (Ngang, Dọc, Chéo) có chiều dài từ 5 đến 9 ô
def evaluate_line(line: List[int], player: int, opponent: int) -> int:
    """Evaluate a single line of length 5 to 9."""
    score = 0 # Khởi tạo điểm số ban đầu = 0
    
    # Biến mảng [0, 1, 1, 1, 0] thành chuỗi "01110" để dễ dàng so khớp (Pattern matching)
    line_str = "".join(str(x) for x in line)
    
    p = str(player) # Ký hiệu quân của AI (Ví dụ: "1")
    o = str(opponent) # Ký hiệu quân của Đối thủ (Ví dụ: "2")
    e = "0" # Ký hiệu ô trống (Empty)
    
    # --- ĐỊNH NGHĨA CÁC MẪU (PATTERN) CỦA AI ---
    # Phép cộng chuỗi tạo ra các hình dạng thế cờ
    p_win = p * 5 # "11111" -> Thắng
    p_open_4 = e + p * 4 + e # "011110" -> 4 quân hở 2 đầu (e = ô trống)
    p_blocked_4_1 = o + p * 4 + e # "211110" -> Bị chặn đầu trái
    p_blocked_4_2 = e + p * 4 + o # "011112" -> Bị chặn đầu phải
    p_open_3 = e + p * 3 + e # "01110" -> 3 quân hở 2 đầu
    p_blocked_3_1 = o + p * 3 + e + e # "211100" -> Bị chặn trái, cần 2 ô trống phải
    p_blocked_3_2 = e + e + p * 3 + o # "001112" -> Bị chặn phải, cần 2 ô trống trái
    p_open_2 = e + e + p * 2 + e + e # "001100" -> 2 quân hở thênh thang
    
    # --- CHẤM ĐIỂM TẤN CÔNG (Lợi thế của AI) ---
    # Quét xem trong chuỗi hiện tại có chứa mẫu nào không, nếu có thì CỘNG ĐIỂM cho AI
    if p_win in line_str: return WIN_SCORE # Thấy đường thắng thì trả về điểm tối đa luôn, không cần tính nữa
    if p_open_4 in line_str: score += OPEN_FOUR 
    if p_blocked_4_1 in line_str or p_blocked_4_2 in line_str: score += BLOCKED_FOUR
    if p_open_3 in line_str: score += OPEN_THREE
    if p_blocked_3_1 in line_str or p_blocked_3_2 in line_str: score += BLOCKED_THREE
    if p_open_2 in line_str: score += OPEN_TWO

    # --- ĐỊNH NGHĨA CÁC MẪU CỦA ĐỐI THỦ ---
    o_win = o * 5 # "22222"
    o_open_4 = e + o * 4 + e # "022220"
    o_blocked_4_1 = p + o * 4 + e # "122220"
    o_blocked_4_2 = e + o * 4 + p # "022221"
    o_open_3 = e + o * 3 + e # "02220"
    
    # --- CHẤM ĐIỂM PHÒNG THỦ (Hiểm họa từ Đối thủ) ---
    # Đây là nguyên tắc Zero-Sum Game: Bất lợi của mình = Lợi thế của địch.
    # Khi đối thủ có thế cờ tốt, AI bị TRỪ ĐIỂM. Điều này ép Minimax phải né các nhánh tương lai mà đối thủ có điểm cao.
    
    if o_win in line_str: return -WIN_SCORE # Nếu địch thắng thì trả về âm tối đa -> Báo hiệu AI thua.
    
    # QUAN TRỌNG: Tại sao lại nhân 2 (OPEN_FOUR * 2)?
    # Vì nếu địch có 4 quân hở 2 đầu, đó là báo động đỏ (sắp chết). 
    # Trừ gấp đôi điểm sẽ ép thuật toán Minimax đánh giá nước đi này cực kỳ tồi tệ, từ đó ưu tiên tìm mọi cách chặn ngay lập tức.
    if o_open_4 in line_str: score -= OPEN_FOUR * 2  
    
    if o_blocked_4_1 in line_str or o_blocked_4_2 in line_str: score -= BLOCKED_FOUR
    
    # Tương tự, nếu địch có OPEN_THREE, nguy cơ thành OPEN_FOUR rất cao, nên trừ gấp đôi điểm để AI lo dập tắt sớm.
    if o_open_3 in line_str: score -= OPEN_THREE * 2

    return score # Trả về tổng điểm của đường thẳng này

# Hàm đánh giá toàn bộ bàn cờ: Cắt ma trận thành các đường thẳng để đưa vào hàm evaluate_line ở trên
def evaluate_board(grid: List[List[int]], size: int, player: int) -> int:
    opponent = 3 - player # Nếu player là 1 thì opponent là 2, và ngược lại.
    total_score = 0 # Tổng điểm của cả bàn cờ
    
    # 1. Quét HÀNG NGANG
    for r in range(size):
        row = grid[r] # Lấy cả hàng ngang
        total_score += evaluate_line(row, player, opponent)
        
    # 2. Quét HÀNG DỌC
    for c in range(size):
        col = [grid[r][c] for r in range(size)] # Trích xuất các phần tử trên cùng cột c
        total_score += evaluate_line(col, player, opponent)
        
    # 3. Quét ĐƯỜNG CHÉO XUÔI (Từ trên-trái xuống dưới-phải)
    # d chạy từ âm sang dương để lấy các đường chéo cắt ngang ma trận
    for d in range(-size + 1, size):
        diag = []
        for r in range(size):
            c = r - d
            if 0 <= c < size: # Nếu tọa độ nằm trong bàn cờ thì lấy ra
                diag.append(grid[r][c])
        # Chỉ đánh giá những đường chéo có độ dài từ 5 trở lên (vì dưới 5 thì không thể tạo thành dãy 5 quân để thắng)
        if len(diag) >= 5:
            total_score += evaluate_line(diag, player, opponent)
            
    # 4. Quét ĐƯỜNG CHÉO NGƯỢC (Từ trên-phải xuống dưới-trái)
    for d in range(2 * size - 1):
        diag = []
        for r in range(size):
            c = d - r
            if 0 <= c < size:
                diag.append(grid[r][c])
        if len(diag) >= 5:
            total_score += evaluate_line(diag, player, opponent)
            
    return total_score # Trả về tổng điểm đánh giá của bàn cờ hiện tại
