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

        #region Làm mới
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

        #region Thêm cạnh
        
        # 1. Label tiêu đề
        self.lbl_ket_noi = ctk.CTkLabel(
            self,
            text="Kết nối đỉnh (Thêm cạnh):",
            font=styles.get_font(size=14, weight="bold"),
            text_color="black",
            anchor="w"
        )
        self.lbl_ket_noi.pack(fill="x", padx=10, pady=0)

        # Frame
        self.frame_action = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_action.pack(fill="x", padx=5, pady=5)

        # 2. Nút Từ Đỉnh (Nằm bên trái)
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

        # 3. Nút Đến Đỉnh (Nằm bên phải)
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

        # Frame 
        self.frame_thuc_hien = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_thuc_hien.pack(fill="x", padx=5, pady=(5, 10))

        # 4. Ô nhập trọng số (Bên trái)
        self.entry_trong_so = ctk.CTkEntry(
            self.frame_thuc_hien,
            placeholder_text="Ví dụ: 10",
            height=40,
            font=styles.get_font(size=13)
        )
        self.entry_trong_so.pack(side="left", fill="x", expand=True, padx=(0, 5))

        # 5. Nút Thêm (Bên phải)
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
    
        #region thêm nút lưu
        # Tạo frame
        self.spacer = ctk.CTkFrame(self, fg_color="transparent")
        self.spacer.pack(fill="both", expand=True)

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

    #endregion


