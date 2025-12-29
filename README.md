# 🧩 MUMMY MAZE

1. GIỚI THIỆU:
Mummy Maze là một game giải đố mê cung được xây dựng bằng Python và thư viện Pygame.
Người chơi điều khiển nhân vật Explorer di chuyển trong mê cung, tránh các Enemy,
sử dụng Key để mở Gate và tìm đường đến Exit để chiến thắng.

2. CẤU TRÚC BÀI NỘP
- Toàn bộ mã nguồn được đặt trong thư mục: source/
- Các thư mục không cần thiết như .vs, .vscode, __pycache__ đã được loại bỏ để giảm dung lượng.

- Cấu trúc chính (rút gọn):
source/
  + main.py
  + path_utils.py
  + game/
  + ui/
  + assets/
  + font/

3. YÊU CẦU MÔI TRƯỜNG
- Python phiên bản khuyến nghị: 3.10 hoặc 3.11
- Hệ điều hành: Windows
- Thư viện sử dụng: pygame

4. CÀI ĐẶT
- Bước 1: Mở Command Prompt (CMD)
- Bước 2: Di chuyển vào thư mục source: Gõ cd source

- Bước 3: (Khuyến nghị) Tạo môi trường ảo, gõ:
  + python -m venv venv
  + venv\\Scripts\\activate

- Bước 4: Cài đặt thư viện cần thiết: Gõ pip install pygame

5. CHẠY GAME
- Trong thư mục source/, chạy lệnh: python main.py

6. HƯỚNG DẪN SỬ DỤNG
- Sử dụng các phím mũi tên (↑ ↓ ← →) để di chuyển Explorer.
- Mỗi bước đi của người chơi sẽ kéo theo lượt di chuyển của Enemy.
- Mục tiêu: đưa Explorer đến Stair để chiến thắng, tránh Trap và Enemy.
- Game hỗ trợ nhiều chức năng cho người dùng tối ưu trải nghiệm.

7. LINK MÃ NGUỒN: 
https://github.com/TinyTech-67311/MummyMaze.git

8. GHI CHÚ
- Đảm bảo chạy chương trình từ đúng thư mục source để tránh lỗi đường dẫn tài nguyên.

