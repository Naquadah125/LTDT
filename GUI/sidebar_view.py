import tkinter as tk
import customtkinter as ctk
from . import styles
from . import sidebar_function 

class Sidebar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#f0f0f0")

        self.tu_dinh_da_chon = None
        self.den_dinh_da_chon = None
        
        # Tiêu đề
        lbl = tk.Label(self, text="Menu", bg="#f0f0f0", font=styles.get_font(size=24, weight="bold"))
        lbl.pack(pady=10)

        #region thêm đỉnh button
        # label Thêm đỉnh
        self.lbl_huong_dan = ctk.CTkLabel(
            self,
            text="Thêm đỉnh vào sơ đồ: ",
            font=styles.get_font(size=14, weight="bold"),
            text_color="black",
            anchor="w"
        )
        self.lbl_huong_dan.pack(fill="x", padx=10, pady=0)

        # btn thêm đỉnh
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

        #region Xóa hết mọi thứ frame
        # Label
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

        #region Thêm cạnh frame
        self.lbl_ket_noi = ctk.CTkLabel(
            self,
            text="Kết nối đỉnh (Thêm cạnh):",
            font=styles.get_font(size=14, weight="bold"),
            text_color="black",
            anchor="w"
        )
        self.lbl_ket_noi.pack(fill="x", padx=10, pady=0)

        # Frame Trên
        self.frame_action = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_action.pack(fill="x", padx=10, pady=5)

        # Nút Từ Đỉnh (Nằm bên trái)
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

        # Nút Đến Đỉnh (Nằm bên phải)
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

        # Frame dưới
        self.frame_thuc_hien = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_thuc_hien.pack(fill="x", padx=10, pady=(5, 10))

        # Ô nhập trọng số (Bên trái)
        self.entry_trong_so = ctk.CTkEntry(
            self.frame_thuc_hien,
            placeholder_text="Ví dụ: 10",
            height=40,
            font=styles.get_font(size=13)
        )
        self.entry_trong_so.pack(side="left", fill="x", expand=True, padx=(0, 5))

        # Nút Thêm (Bên phải)
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

        # Frame cho việc chọn thuật toán
        self.frame_header_algo = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_header_algo.pack(fill="x", padx=10, pady=(20, 0))

        # Label Thuật toán
        self.lbl_thuat_toan = ctk.CTkLabel(
            self.frame_header_algo,
            text="Thuật toán: ",    
            font=styles.get_font(size=14, weight="bold"),
            text_color="black",
            anchor="w"
        )
        self.lbl_thuat_toan.pack(side="left")

        # Dropdown Box chọn thuật toán
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

        # Frame chứa 2 nút chọn đỉnh
        self.frame_algo_select = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_algo_select.pack(fill="x", padx=10, pady=5)

        # Nút chọn điểm Bắt đầu
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

        # Nút chọn điểm Kết thúc
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

        # 3. Nút Hành động thực thi
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

        #region Chọn Node
        # Label Lộ trình đi qua
        self.lbl_chon_lo_trinh = ctk.CTkLabel(
            self,
            text="Chọn thứ tự đỉnh đi qua:",
            font=styles.get_font(size=14, weight="bold"),
            text_color="black",
            anchor="w"
        )
        self.lbl_chon_lo_trinh.pack(fill="x", padx=10, pady=(10, 0))

        # Frame
        self.frame_chon_node = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_chon_node.pack(fill="x", padx=10, pady=(5, 10))
        self.frame_chon_node.columnconfigure(0, weight=9)
        self.frame_chon_node.columnconfigure(1, weight=1)

        # Dropdown Box (Liệt kê Nodes)
        self.option_list_node = ctk.CTkOptionMenu(
            self.frame_chon_node,
            values=[], # Sẽ cập nhật sau
            height=40,
            font=styles.get_font(size=14),
            fg_color="#555555",
            button_color="#333333",
            button_hover_color="#222222"
        )
        self.option_list_node.grid(row=0, column=0, sticky="ew", padx=(0, 5))

        # Nút "Thêm"
        self.btn_them_node_list = ctk.CTkButton(
            self.frame_chon_node,
            text="Thêm",
            width=60,
            height=40,
            font=styles.get_font(size=13, weight="bold"),
            fg_color="#27AE60",
            hover_color="#2ECC71"
        )
        self.btn_them_node_list.grid(row=0, column=1, sticky="ew")

        #endregion

        #region thêm nút lưu
        # Nút Lưu
        self.btn_luu_file = ctk.CTkButton(
            self,
            text="Lưu File",
            width=120,
            height=40,
            font=styles.get_font(size=13, weight="bold"),
            fg_color="#F39C12",
            hover_color="#D68910",
            corner_radius=10
        )
        self.btn_luu_file.pack(side="bottom", anchor="e", padx=20, pady=20)

        #endregion



    #region sidebar_function stuff
    def cap_nhat_nut_tu_dinh(self, ten_dinh):
        sidebar_function.cap_nhat_tu_dinh(self, ten_dinh)

    def cap_nhat_nut_den_dinh(self, ten_dinh):
        sidebar_function.cap_nhat_den_dinh(self, ten_dinh)

    def reset_form_nhap_lieu(self):
        sidebar_function.reset_form(self)

    def thay_doi_ten_nut_chay(self, gia_tri_chon):
        """Hàm này tự động chạy khi Dropdown thay đổi giá trị"""
        
        # Cập nhật text cho nút ở thuật toán
        self.btn_run_algorithm.configure(text=f"Chạy {gia_tri_chon}")

    #endregion


