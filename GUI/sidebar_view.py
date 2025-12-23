import tkinter as tk
import customtkinter as ctk
from . import styles
from . import sidebar_function

class Sidebar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#f0f0f0")

        self.tu_dinh_da_chon = None
        self.den_dinh_da_chon = None
        self.algo_start_node = None
        self.algo_end_node = None
        
        # Tiêu đề
        lbl = tk.Label(self, text="Menu", bg="#f0f0f0", font=styles.get_font(size=24, weight="bold"))
        lbl.pack(pady=10)

        #region thêm đỉnh button
        self.frame_header_them_dinh = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_header_them_dinh.pack(fill="x", padx=10, pady=0)

        self.lbl_huong_dan = ctk.CTkLabel(
            self.frame_header_them_dinh,
            text="Thêm đỉnh vào sơ đồ: ",
            font=styles.get_font(size=14, weight="bold"),
            text_color="black",
            anchor="w"
        )
        self.lbl_huong_dan.pack(side="left")

        # nút toggle
        self.btn_move_node = ctk.CTkButton(
            self.frame_header_them_dinh,
            text="Di chuyển",
            width=80,
            height=20,
            font=styles.get_font(size=13, weight="bold"),
            fg_color="#9B9B9B",
            hover_color="#827979",
            corner_radius=5
        )
        self.btn_move_node.pack(side="right", padx=(5, 0))

        self.btn_them_dinh = ctk.CTkButton(
            self,
            text="Bấm vào đây để thêm đỉnh",
            height=50,
            font=styles.get_font(size=16, weight="bold"),
            fg_color="#3B8ED0",
            hover_color="#1F6AA5",
            corner_radius=10
        )
        self.btn_them_dinh.pack(fill="x", padx=10, pady=0)

        #endregion

        #region Xóa hết mọi thứ
        self.lbl_xoa_dinh = ctk.CTkLabel(
            self,
            text="Làm mới sơ đồ: ",
            font=styles.get_font(size=14, weight="bold"),
            text_color="black",
            anchor="w"
        )
        self.lbl_xoa_dinh.pack(fill="x", padx=10, pady=(20, 0))

        self.btn_xoa_dinh = ctk.CTkButton(
            self,
            text="Xóa tất cả (Reset)",
            height=50,
            font=styles.get_font(size=16, weight="bold"),
            fg_color="#E74C3C",
            hover_color="#C0392B",
            corner_radius=10
        )
        self.btn_xoa_dinh.pack(fill="x", padx=10, pady=(0, 10))

        #endregion

        #region Nối đỉnh
        self.frame_header_ket_noi = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_header_ket_noi.pack(fill="x", padx=10, pady=0)

        self.lbl_ket_noi = ctk.CTkLabel(
            self.frame_header_ket_noi,
            text="Kết nối đỉnh (Thêm cạnh):",
            font=styles.get_font(size=14, weight="bold"),
            text_color="black",
            anchor="w"
        )
        self.lbl_ket_noi.pack(side="left")

        # Refresh button
        self.btn_reset_ket_noi = ctk.CTkButton(
            self.frame_header_ket_noi,
            text="Refresh",
            width=30,
            height=30,
            font=styles.get_font(size=13, weight="bold"),
            fg_color="#7F8C8D",
            hover_color="#95A5A6"
        )
        self.btn_reset_ket_noi.pack(side="right", padx=(5, 0))
        self.btn_reset_ket_noi.configure(command=self.reset_form_nhap_lieu)

        # Frame chứa 2 nút chọn đỉnh
        self.frame_action = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_action.pack(fill="x", padx=10, pady=5)

        self.btn_tu_dinh = ctk.CTkButton(
            self.frame_action,
            text="Từ đỉnh: ?",
            height=40,
            font=styles.get_font(size=15, weight="bold"),
            fg_color="#555555", 
            hover_color="#333333",
            anchor="w"
        )
        self.btn_tu_dinh.pack(side="left", fill="x", expand=True, padx=(0, 2))

        self.btn_den_dinh = ctk.CTkButton(
            self.frame_action,
            text="Đến đỉnh: ?",
            height=40,
            font=styles.get_font(size=15, weight="bold"),
            fg_color="#555555", 
            hover_color="#333333",
            anchor="w"
        )
        self.btn_den_dinh.pack(side="right", fill="x", expand=True, padx=(2, 0))

        # Frame chứa ô nhập và nút Thêm
        self.frame_thuc_hien = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_thuc_hien.pack(fill="x", padx=10, pady=(5, 10))

        self.entry_trong_so = ctk.CTkEntry(
            self.frame_thuc_hien,
            placeholder_text="Ví dụ: 10",
            height=40,
            font=styles.get_font(size=13)
        )
        self.entry_trong_so.pack(side="left", fill="x", expand=True, padx=(0, 5))

        self.btn_them_canh = ctk.CTkButton(
            self.frame_thuc_hien,
            text="THÊM",
            width=80,
            height=40,
            font=styles.get_font(size=13, weight="bold"),
            fg_color="#27AE60",
            hover_color="#2ECC71",
            corner_radius=10
        )
        self.btn_them_canh.pack(side="right", padx=0)

        #endregion
    
        #region Thuật toán selection
        # Frame header thuật toán
        self.frame_header_algo = ctk.CTkFrame(self, fg_color="transparent") # Frame
        self.frame_header_algo.pack(fill="x", padx=10, pady=(20, 0))

        self.lbl_thuat_toan = ctk.CTkLabel(
            self.frame_header_algo,
            text="Thuật toán: ",    
            font=styles.get_font(size=14, weight="bold"),
            text_color="black",
            anchor="w"
        )
        self.lbl_thuat_toan.pack(side="left")

        self.option_thuat_toan = ctk.CTkOptionMenu(
            self.frame_header_algo,
            values=["Dijkstra", "Traveling Salesman"], # Tạm để danh sách mẫu
            command=self.thay_doi_ten_nut_chay,
            height=30,
            font=styles.get_font(size=13),
            fg_color="#555555",
            button_color="#333333",
            button_hover_color="#222222"
        )
        self.option_thuat_toan.pack(side="left", fill="x", expand=True, padx=(10, 0))

        # Nút làm mới
        self.btn_reset_algo = ctk.CTkButton(
            self.frame_header_algo,
            text="Refresh",
            width=30,
            height=30,
            font=styles.get_font(size=13, weight="bold"),
            fg_color="#7F8C8D",
            hover_color="#95A5A6"
        )
        self.btn_reset_algo.pack(side="right", padx=(5, 0))

        # Frame chứa 2 nút chọn đỉnh
        self.frame_algo_select = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_algo_select.pack(fill="x", padx=10, pady=5)

        self.btn_start_node = ctk.CTkButton(
            self.frame_algo_select,
            text="Bắt đầu: ?",
            height=40,
            font=styles.get_font(size=15, weight="bold"),
            fg_color="#555555", 
            hover_color="#333333",
            anchor="w"
        )
        self.btn_start_node.pack(side="left", fill="x", expand=True, padx=(0, 2))

        self.btn_end_node = ctk.CTkButton(
            self.frame_algo_select,
            text="Kết thúc: ?",
            height=40,
            font=styles.get_font(size=15, weight="bold"),
            fg_color="#555555", 
            hover_color="#333333",
            anchor="w"
        )
        self.btn_end_node.pack(side="right", fill="x", expand=True, padx=(2, 0))

        self.btn_run_algorithm = ctk.CTkButton(
            self,
            text="Chạy Dijkstra", # Đổi tên nút ở đây
            height=40,
            font=styles.get_font(size=15, weight="bold"),
            fg_color="#27AE60",
            hover_color="#237A47",
            corner_radius=10
        )
        self.btn_run_algorithm.pack(fill="x", padx=10, pady=(5, 10))

        #endregion

        #region Khu vực hiển thị kết quả thuật toán
        # Frame chứa toàn bộ phần kết quả
        self.frame_result_top = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=8)
        self.frame_result_top.pack(fill="x", pady=(5, 5))

        self.lbl_kq_title = ctk.CTkLabel(
            self.frame_result_top,
            text="Kết quả:",
            font=styles.get_font(size=14, weight="bold"),
            text_color="#000000",
            anchor="w"
        )
        self.lbl_kq_title.pack(fill="x", padx=8, pady=(8, 0))

        self.lbl_chi_phi = ctk.CTkLabel(
            self.frame_result_top,
            text="Chi phí: -",
            font=styles.get_font(size=13, weight="bold"),
            text_color="#FF0000",
            anchor="w"
        )
        self.lbl_chi_phi.pack(fill="x", padx=8, pady=0)

        self.lbl_lo_trinh = ctk.CTkLabel(
            self.frame_result_top,
            text="Lộ trình: -",
            font=styles.get_font(size=13, weight="bold"),
            text_color="#FF0000",
            anchor="w",
            wraplength=240,
            justify="left"
        )
        self.lbl_lo_trinh.pack(fill="x", padx=8, pady=0)

        #endregion

#region thêm nút lưu, load file, hiện thị chi tiết
        
        # Tạo một frame tổng ở dưới đáy để chứa 2 dòng nút
        self.frame_bottom_area = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_bottom_area.pack(side="bottom", fill="x", padx=10, pady=(10, 20))

        # --- DÒNG 1: Nút Chi tiết thông tin ---
        self.btn_chi_tiet_thong_tin = ctk.CTkButton(
            self.frame_bottom_area,
            text="Chi tiết thông tin",
            height=40,
            font=styles.get_font(size=13, weight="bold"),
            fg_color="#8E44AD",
            hover_color="#6C3483",
            corner_radius=10
        )
        # pack(fill="x") để nút tự giãn ra cho đẹp
        self.btn_chi_tiet_thong_tin.pack(side="top", fill="x", pady=(0, 10)) 

        # --- DÒNG 2: Chứa nút Lưu và Load ---
        self.frame_file_actions = ctk.CTkFrame(self.frame_bottom_area, fg_color="transparent")
        self.frame_file_actions.pack(side="top", fill="x")

        # Lưu File (Bên trái)
        self.btn_luu_file = ctk.CTkButton(
            self.frame_file_actions,
            text="Lưu",
            width=80, # Giảm width xuống một chút
            height=40,
            font=styles.get_font(size=13, weight="bold"),
            fg_color="#F39C12",
            hover_color="#D68910",
            corner_radius=10
        )
        self.btn_luu_file.pack(side="left", fill="x", expand=True, padx=(0, 5))

        # Load File (Bên phải)
        self.btn_load_file = ctk.CTkButton(
            self.frame_file_actions,
            text="Load",
            width=80, # Giảm width xuống
            height=40,
            font=styles.get_font(size=13, weight="bold"),
            fg_color="#3498DB",
            hover_color="#2980B9",
            corner_radius=10
        )
        self.btn_load_file.pack(side="right", fill="x", expand=True, padx=(5, 0))

        #endregion

    #region sidebar_function stuff
    def cap_nhat_nut_tu_dinh(self, ten_dinh):
        sidebar_function.cap_nhat_tu_dinh(self, ten_dinh)

    def cap_nhat_nut_den_dinh(self, ten_dinh):
        sidebar_function.cap_nhat_den_dinh(self, ten_dinh)

    def reset_form_nhap_lieu(self):
        sidebar_function.reset_form_noi_dinh(self)

    def thay_doi_ten_nut_chay(self, gia_tri_chon):
        """Hàm này tự động chạy khi dropdown thay đổi giá trị"""
        # Cập nhật text cho nút
        self.btn_run_algorithm.configure(text=f"Chạy {gia_tri_chon}")

        if gia_tri_chon == "Traveling Salesman":
            # Nếu là TSP: Ẩn nút Kết thúc đi
            self.btn_end_node.pack_forget()
            self.algo_end_node = None 
            
        elif gia_tri_chon == "Dijkstra":
            # Nếu là Dijkstra: Hiện nút Kết thúc lại
            self.btn_end_node.pack(side="right", fill="x", expand=True, padx=(2, 0))

    def cap_nhat_algo_start(self, ten_dinh):
        self.algo_start_node = ten_dinh
        self.btn_start_node.configure(
            text=f"Bắt đầu: {ten_dinh}", 
            fg_color="#34F222",
            hover_color="#2ECC71"
        )

    def cap_nhat_algo_end(self, ten_dinh):
        self.algo_end_node = ten_dinh
        self.btn_end_node.configure(
            text=f"Kết thúc: {ten_dinh}", 
            fg_color="#34F222",
            hover_color="#2ECC71"
        )

    def reset_algo_ui(self):
        """Reset giao diện phần thuật toán về mặc định"""
        self.algo_start_node = None
        self.algo_end_node = None

        self.btn_start_node.configure(
            text="Bắt đầu: ?", 
            fg_color="#555555",
            hover_color="#333333"
        )
        self.btn_end_node.configure(
            text="Kết thúc: ?", 
            fg_color="#555555",
            hover_color="#333333"
        )

        # Reset dropdown về Dijkstra
        self.option_thuat_toan.set("Dijkstra")
        self.thay_doi_ten_nut_chay("Dijkstra")

    def hien_thi_ket_qua(self, chi_phi, path_nodes, algo_name=""):
        """Hiển thị kết quả ở phần kết quả sidebar"""
        try:
            self.lbl_chi_phi.configure(text=f"Chi phí: {chi_phi}")
            self.lbl_lo_trinh.configure(text=f"Lộ trình: {' -> '.join(path_nodes)}")
        except AttributeError:
            # Nếu phần UI chưa được tạo, bỏ qua một cách an toàn
            pass

    def xoa_ket_qua(self):
        """Xóa/Reset phần hiển thị kết quả"""
        try:
            self.lbl_chi_phi.configure(text="Chi phí: -")
            self.lbl_lo_trinh.configure(text="Lộ trình: -")
        except AttributeError:
            pass

    #endregion


