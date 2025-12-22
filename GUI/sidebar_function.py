import customtkinter as ctk

def cap_nhat_tu_dinh(sidebar_ui, ten_dinh):
    """Cập nhật nút Từ Đỉnh"""
    sidebar_ui.tu_dinh_da_chon = ten_dinh
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

def reset_form_noi_dinh(sidebar_ui):
    """Reset form về trạng thái ban đầu"""
    # Xóa dữ liệu
    sidebar_ui.tu_dinh_da_chon = None
    sidebar_ui.den_dinh_da_chon = None

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

    # Xóa số
    sidebar_ui.entry_trong_so.delete(0, "end")

def thay_doi_ten_nut_chay(sidebar_ui, gia_tri_chon):
    """Hàm này tự động chạy khi DropdownBox của thuật toán thay đổi giá trị"""
    sidebar_ui.btn_run_algorithm.configure(text=f"Chạy {gia_tri_chon}")

def cap_nhat_algo_start(sidebar_ui, ten_dinh):
    """Cập nhật nút Bắt đầu"""
    sidebar_ui.algo_start_node = ten_dinh
    sidebar_ui.btn_start_node.configure(
        text=f"Bắt đầu: {ten_dinh}",
        fg_color="#8E44AD"
    )

def cap_nhat_algo_end(sidebar_ui, ten_dinh):
    """Cập nhật nút Kết thúc"""
    sidebar_ui.algo_end_node = ten_dinh
    sidebar_ui.btn_end_node.configure(
        text=f"Kết thúc: {ten_dinh}",
        fg_color="#8E44AD"
    )

