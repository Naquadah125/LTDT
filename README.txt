LÝ THUYẾT ĐỒ THỊ

INSTALLATION GUIDE:
Bước 1: Cài đặt Python
Tải Python (bản 3.10 trở lên) tại: https://www.python.org/downloads/
   Quan trọng: Khi cài đặt, NHỚ tích vào ô "Add Python to PATH".

Bước 2: Tải Source Code từ GitHub
Mở Terminal,và chạy lệnh sau để tải mã nguồn về máy:
   git clone https://github.com/Naquadah125/LTDT.git

Bước 3: Tạo môi trường ảo (Virtual Environment)
Chạy lệnh:
   python -m venv .venv

Bước 4: Kích hoạt môi trường ảo
Chạy lệnh:
   .venv\Scripts\activate

Bước 5: Cài đặt thư viện
Chạy lệnh:
   pip install -r requirements.txt

Bước 6: Chạy ứng dụng
Chạy lệnh:
   python app.py

Bước 7: Thực hành
   Thêm đỉnh
      Bấm vào phần 'Thêm đỉnh' để chuyển qua chế độ add đỉnh vào canvas bên trái, thêm ít nhất 2 điểm
   Nối đỉnh:
      Bấm vào 'Từ đỉnh: ?' và chọn 1 đỉnh ở phần canvas, đây sẽ là điểm bắt đầu
      Bấm vài 'Đến đỉnh: ?' và chọn 1 đỉnh khác ở canvas, đây sẽ là điểm kết thúc 
      Gắn 1 giá trị số vào phần textBox gần nút 'THÊM' để gắn giá trị trọng số
   Lưu File:
      Khi xong ta bấm vào nút 'lưu file' ở góc dưới phải, sẽ lưu lại biểu đồ với số liệu
