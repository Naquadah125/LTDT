import customtkinter as ctk

COLOR_NORMAL = "#ECF0F1"       
COLOR_TEXT_NORMAL = "#2C3E50"  

COLOR_SELECTED = "#2C3E50"     
COLOR_TEXT_SELECTED = "#FFFFFF"

def cap_nhat_tu_dinh(sidebar_ui, ten_dinh):
    sidebar_ui.tu_dinh_da_chon = ten_dinh
    sidebar_ui.btn_tu_dinh.configure(
        text=f"{ten_dinh}",
        fg_color=COLOR_SELECTED,
        text_color=COLOR_TEXT_SELECTED
    )

def cap_nhat_den_dinh(sidebar_ui, ten_dinh):
    sidebar_ui.den_dinh_da_chon = ten_dinh
    sidebar_ui.btn_den_dinh.configure(
        text=f"{ten_dinh}",
        fg_color=COLOR_SELECTED,
        text_color=COLOR_TEXT_SELECTED
    )

def reset_form_noi_dinh(sidebar_ui):
    sidebar_ui.tu_dinh_da_chon = None
    sidebar_ui.den_dinh_da_chon = None

    sidebar_ui.btn_tu_dinh.configure(
        text="Từ...",
        fg_color=COLOR_NORMAL,
        text_color=COLOR_TEXT_NORMAL
    )
    sidebar_ui.btn_den_dinh.configure(
        text="Đến...",
        fg_color=COLOR_NORMAL,
        text_color=COLOR_TEXT_NORMAL
    )

    sidebar_ui.entry_trong_so.delete(0, "end")

def cap_nhat_algo_start(sidebar_ui, ten_dinh):
    """Cập nhật nút Bắt đầu thuật toán"""
    sidebar_ui.algo_start_node = ten_dinh
    sidebar_ui.btn_start_node.configure(
        text=f"{ten_dinh}", # Chỉ hiện tên đỉnh
        fg_color=COLOR_SELECTED,
        text_color=COLOR_TEXT_SELECTED
    )

def cap_nhat_algo_end(sidebar_ui, ten_dinh):
    """Cập nhật nút Kết thúc thuật toán"""
    sidebar_ui.algo_end_node = ten_dinh
    sidebar_ui.btn_end_node.configure(
        text=f"{ten_dinh}", # Chỉ hiện tên đỉnh
        fg_color=COLOR_SELECTED,
        text_color=COLOR_TEXT_SELECTED
    )