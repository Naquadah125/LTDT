import json

def cap_nhat_tu_dinh(sidebar_ui, ten_dinh):
    """Cập nhật nút Từ Đỉnh"""
    # Lưu dữ liệu vào biến của sidebar
    sidebar_ui.tu_dinh_da_chon = ten_dinh
    
    # Cập nhật giao diện nút
    sidebar_ui.btn_tu_dinh.configure(
        text=f"Từ đỉnh: {ten_dinh}",
        fg_color="#34F222",
        hover_color="#2ECC71"
    )

def cap_nhat_den_dinh(sidebar_ui, ten_dinh):
    """Cập nhật nút Đến Đỉnh"""
    sidebar_ui.den_dinh_da_chon = ten_dinh
    
    sidebar_ui.btn_den_dinh.configure(
        text=f"Đến đỉnh: {ten_dinh}",
        fg_color="#34F222",
        hover_color="#2ECC71"
    )

def reset_form(sidebar_ui):
    """Reset form về trạng thái ban đầu"""
    # 1. Xóa dữ liệu
    sidebar_ui.tu_dinh_da_chon = None
    sidebar_ui.den_dinh_da_chon = None

    # 2. Reset nút về màu xám
    sidebar_ui.btn_tu_dinh.configure(
        text="Từ đỉnh: ?",
        fg_color="#555555",
        hover_color="#333333"
    )
    
    sidebar_ui.btn_den_dinh.configure(
        text="Đến đỉnh: ?",
        fg_color="#555555",
        hover_color="#333333"
    )

    # 3. Xóa ô nhập
    sidebar_ui.entry_trong_so.delete(0, "end")
    
