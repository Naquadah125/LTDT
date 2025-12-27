import tkinter as tk
import customtkinter as ctk
from . import styles
from . import sidebar_function

THEME_BG = "#4e5b91"
THEME_BTN_NORMAL = "#ECF0F1"
THEME_BTN_HOVER = "#BDC3C7"
THEME_BTN_ACTIVE = "#2C3E50"
THEME_TEXT_HEADER = "#FFFFFF"
THEME_TEXT_BTN = "#2C3E50"

BTN_H = 28
PAD_X = 10
FIXED_W = 60

class Sidebar(ctk.CTkFrame):    
    def __init__(self, parent):
        super().__init__(parent, fg_color=THEME_BG, corner_radius=0)

        self.tu_dinh_da_chon = None
        self.den_dinh_da_chon = None
        self.algo_start_node = None
        self.algo_end_node = None
        
        self.lbl_title = ctk.CTkLabel(
            self, 
            text="====== M E N U ======", 
            font=("Montserrat", 20, "bold"),
            text_color=THEME_TEXT_HEADER
        )
        self.lbl_title.pack(pady=(15, 15))

        #region Cài đặt chung
        self.frame_header_dinh = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_header_dinh.pack(fill="x", padx=PAD_X, pady=(5, 2))

        self.lbl_dinh = ctk.CTkLabel(
            self.frame_header_dinh, text="Cài đặt chung", 
            font=styles.get_font(size=12, weight="bold"),
            text_color=THEME_TEXT_HEADER, anchor="w"
        )
        self.lbl_dinh.pack(side="left")

        # Nút Thêm Đỉnh
        self.btn_them_dinh = ctk.CTkButton(
            self,
            text="Thêm mới đỉnh", 
            height=BTN_H,
            font=styles.get_font(size=12, weight="bold"),
            fg_color=THEME_BTN_NORMAL, text_color=THEME_TEXT_BTN, hover_color=THEME_BTN_HOVER,
            corner_radius=6
        )
        self.btn_them_dinh.pack(fill="x", padx=PAD_X, pady=(0, 5))

        # Nút di chuyển
        self.btn_move_node = ctk.CTkButton(
            self,
            text="Di chuyển đỉnh", 
            height=BTN_H,
            font=styles.get_font(size=12, weight="bold"),
            fg_color=THEME_BTN_NORMAL, text_color=THEME_TEXT_BTN, hover_color=THEME_BTN_HOVER,
            corner_radius=6
        )
        self.btn_move_node.pack(fill="x", padx=PAD_X, pady=(0, 5))

        # Nút Thông tin
        self.btn_thong_tin = ctk.CTkButton(
            self,
            text="Thông tin chung",
            height=BTN_H,
            font=styles.get_font(size=12, weight="bold"),
            fg_color=THEME_BTN_NORMAL, text_color=THEME_TEXT_BTN, hover_color=THEME_BTN_HOVER,
            corner_radius=6
        )
        self.btn_thong_tin.pack(fill="x", padx=PAD_X, pady=(0, 5))

        #endregion

        #region Chỉnh sửa đỉnh
        self.frame_chinh_sua = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_chinh_sua.pack(fill="x", padx=PAD_X, pady=(5, 2))

        self.lbl_dinh = ctk.CTkLabel(
            self.frame_chinh_sua, text="Xóa", 
            font=styles.get_font(size=12, weight="bold"),
            text_color=THEME_TEXT_HEADER, anchor="w"
        )
        self.lbl_dinh.pack(side="left")

        # Nút Làm mới
        self.btn_xoa_dinh = ctk.CTkButton(
            self,
            text="Làm mới đồ thị",
            height=BTN_H,
            font=styles.get_font(size=12, weight="bold"),
            fg_color=THEME_BTN_NORMAL, text_color=THEME_TEXT_BTN, hover_color=THEME_BTN_HOVER,
            corner_radius=6
        )
        self.btn_xoa_dinh.pack(fill="x", padx=PAD_X, pady=(0, 5))

        # Nút Undo
        self.btn_undo = ctk.CTkButton(
            self,
            text="Hoàn tác ",
            height=BTN_H,
            font=styles.get_font(size=12, weight="bold"),
            fg_color=THEME_BTN_NORMAL, text_color=THEME_TEXT_BTN, hover_color=THEME_BTN_HOVER,
            corner_radius=6
        )
        self.btn_undo.pack(fill="x", padx=PAD_X, pady=(0, 5))

        #endregion

        #region Cạnh
        self.create_header_label("Cạnh")
        self.frame_inputs = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_inputs.pack(fill="x", padx=PAD_X, pady=(0, 5))
        
        self.frame_inputs.columnconfigure(0, weight=1, uniform="group_inputs") 
        self.frame_inputs.columnconfigure(1, weight=0)
        self.frame_inputs.columnconfigure(2, weight=1, uniform="group_inputs")

        self.btn_tu_dinh = ctk.CTkButton(
            self.frame_inputs,
            text="Từ...",
            height=BTN_H, width=FIXED_W, 
            font=styles.get_font(size=11, weight="bold"),
            fg_color=THEME_BTN_NORMAL, text_color=THEME_TEXT_BTN, hover_color=THEME_BTN_HOVER
        )
        self.btn_tu_dinh.grid(row=0, column=0, sticky="ew", padx=(0, 2))

        self.entry_trong_so = ctk.CTkEntry(
            self.frame_inputs,
            placeholder_text="0",
            width=50, height=BTN_H, 
            justify="center",
            font=styles.get_font(size=11, weight="bold"),
            border_width=0,
            fg_color=THEME_BTN_NORMAL, text_color=THEME_TEXT_BTN
        )
        self.entry_trong_so.grid(row=0, column=1, padx=2)

        self.btn_den_dinh = ctk.CTkButton(
            self.frame_inputs,
            text="Đến...",
            height=BTN_H, width=FIXED_W,
            font=styles.get_font(size=11, weight="bold"),
            fg_color=THEME_BTN_NORMAL, text_color=THEME_TEXT_BTN, hover_color=THEME_BTN_HOVER
        )
        self.btn_den_dinh.grid(row=0, column=2, sticky="ew", padx=(2, 0))

        self.frame_edge_actions = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_edge_actions.pack(fill="x", padx=PAD_X, pady=(0, 5))

        self.btn_them_canh = ctk.CTkButton(
            self.frame_edge_actions,
            text="Thêm",
            height=BTN_H, width=FIXED_W,
            font=styles.get_font(size=12, weight="bold"),
            fg_color=THEME_BTN_ACTIVE, text_color="white", hover_color="#1A252F",
            corner_radius=6
        )
        self.btn_them_canh.pack(side="left", fill="x", expand=True, padx=(0, 2))

        self.btn_reset_ket_noi = ctk.CTkButton(
            self.frame_edge_actions,
            text="⟳", width=30, height=BTN_H,
            font=styles.get_font(size=14, weight="bold"),
            fg_color=THEME_BTN_NORMAL, text_color=THEME_TEXT_BTN, hover_color=THEME_BTN_HOVER,
            corner_radius=6
        )
        self.btn_reset_ket_noi.pack(side="right")
        
        #endregion

        #region Thuật toán
        self.create_header_label("Thuật toán")

        self.option_thuat_toan = ctk.CTkOptionMenu(
            self,
            values=["Dijkstra", "TSP"],
            command=self.thay_doi_ten_nut_chay,
            height=BTN_H,
            font=styles.get_font(size=11),
            fg_color=THEME_BTN_NORMAL, button_color=THEME_BTN_HOVER, button_hover_color=THEME_BTN_HOVER,
            text_color=THEME_TEXT_BTN, dropdown_fg_color=THEME_BTN_NORMAL, dropdown_text_color=THEME_TEXT_BTN,
        )
        self.option_thuat_toan.pack(fill="x", padx=PAD_X, pady=(0, 5))

        self.frame_algo_select = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_algo_select.pack(fill="x", padx=PAD_X, pady=(0, 5))
        self.frame_algo_select.columnconfigure(0, weight=1, uniform="group_algo")
        self.frame_algo_select.columnconfigure(1, weight=1, uniform="group_algo")

        self.btn_start_node = ctk.CTkButton(
            self.frame_algo_select, text="Từ...", 
            height=BTN_H, width=FIXED_W,
            font=styles.get_font(size=11, weight="bold"),
            fg_color=THEME_BTN_NORMAL, text_color=THEME_TEXT_BTN, hover_color=THEME_BTN_HOVER
        )
        self.btn_start_node.grid(row=0, column=0, sticky="ew", padx=(0, 2))

        self.btn_end_node = ctk.CTkButton(
            self.frame_algo_select, text="Đến...", 
            height=BTN_H, width=FIXED_W,
            font=styles.get_font(size=11, weight="bold"),
            fg_color=THEME_BTN_NORMAL, text_color=THEME_TEXT_BTN, hover_color=THEME_BTN_HOVER
        )
        self.btn_end_node.grid(row=0, column=1, sticky="ew", padx=(2, 0))

        self.frame_run_algo = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_run_algo.pack(fill="x", padx=PAD_X, pady=(5, 5))

        self.btn_run_algorithm = ctk.CTkButton(
            self.frame_run_algo, text="Chạy", 
            height=BTN_H, width=FIXED_W,
            font=styles.get_font(size=12, weight="bold"),
            fg_color=THEME_BTN_ACTIVE, text_color="white", hover_color="#1A252F",
            corner_radius=6
        )
        self.btn_run_algorithm.pack(side="left", padx=(0, 2), expand=True, fill="x")

        self.btn_reset_algo = ctk.CTkButton(
            self.frame_run_algo, text="⟳", width=30, height=BTN_H,
            font=styles.get_font(size=14, weight="bold"),
            fg_color=THEME_BTN_NORMAL, text_color=THEME_TEXT_BTN, hover_color=THEME_BTN_HOVER,
            corner_radius=6
        )
        self.btn_reset_algo.pack(side="right")
        
        #endregion

        #region Kết quả
        self.frame_result = ctk.CTkFrame(self, fg_color="white", corner_radius=6)
        self.frame_result.pack(fill="x", padx=PAD_X, pady=(10, 5))
        
        self.lbl_chi_phi = ctk.CTkLabel(self.frame_result, text="Chi phí: -", text_color="black", anchor="w", font=styles.get_font(size=13, weight="bold"))
        self.lbl_chi_phi.pack(fill="x", padx=5, pady=(2, 0))
        
        self.lbl_lo_trinh = ctk.CTkLabel(self.frame_result, text="Lộ trình: -", text_color="black", anchor="w", font=styles.get_font(size=13, weight="bold"))
        self.lbl_lo_trinh.pack(fill="x", padx=5, pady=(0, 2))
        
        #endregion

        #region lưu / load file
        self.frame_footer = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_footer.pack(side="bottom", fill="x", padx=PAD_X, pady=10)

        self.btn_luu_file = ctk.CTkButton(
            self.frame_footer, text="Lưu", height=32, width=30,
            font=styles.get_font(size=16, weight="bold"), fg_color=THEME_BTN_NORMAL, text_color=THEME_TEXT_BTN, hover_color=THEME_BTN_HOVER
        )
        self.btn_luu_file.pack(side="left", fill="x", expand=True, padx=(0, 2))

        self.btn_load_file = ctk.CTkButton(
            self.frame_footer, text="Load", height=32, width=30,
            font=styles.get_font(size=16, weight="bold"), fg_color=THEME_BTN_NORMAL, text_color=THEME_TEXT_BTN, hover_color=THEME_BTN_HOVER
        )
        self.btn_load_file.pack(side="right", fill="x", expand=True, padx=(2, 0))
        
        #endregion

    #region function tạo UI
    def create_header_label(self, text):
        lbl = ctk.CTkLabel(
            self, text=text, 
            font=styles.get_font(size=12, weight="bold"),
            text_color=THEME_TEXT_HEADER, anchor="w"
        )
        lbl.pack(fill="x", padx=PAD_X, pady=(15, 2))
    
    #endregion

    #region function helper
    def cap_nhat_nut_tu_dinh(self, ten_dinh):
        sidebar_function.cap_nhat_tu_dinh(self, ten_dinh)

    def cap_nhat_nut_den_dinh(self, ten_dinh):
        sidebar_function.cap_nhat_den_dinh(self, ten_dinh)

    def reset_form_nhap_lieu(self):
        sidebar_function.reset_form_noi_dinh(self)

    def thay_doi_ten_nut_chay(self, gia_tri_chon):
        self.btn_run_algorithm.configure(text="Chạy")
        if gia_tri_chon == "TSP":
            self.btn_end_node.grid_forget()
            self.algo_end_node = None 
        elif gia_tri_chon == "Dijkstra":
            self.btn_end_node.grid(row=0, column=1, sticky="ew", padx=(2, 0))

    def cap_nhat_algo_start(self, ten_dinh):
        sidebar_function.cap_nhat_algo_start(self, ten_dinh)

    def cap_nhat_algo_end(self, ten_dinh):
        sidebar_function.cap_nhat_algo_end(self, ten_dinh)

    def reset_algo_ui(self):
        self.algo_start_node = None
        self.algo_end_node = None
        self.btn_start_node.configure(text="Từ...", fg_color=THEME_BTN_NORMAL, text_color=THEME_TEXT_BTN)
        self.btn_end_node.configure(text="Đến...", fg_color=THEME_BTN_NORMAL, text_color=THEME_TEXT_BTN)
        self.option_thuat_toan.set("Dijkstra")
        self.thay_doi_ten_nut_chay("Dijkstra")

    def hien_thi_ket_qua(self, chi_phi, path_nodes, algo_name=""):
        try:
            self.lbl_chi_phi.configure(text=f"Chi phí: {chi_phi}")
            self.lbl_lo_trinh.configure(text=f"Lộ trình: {' -> '.join(path_nodes)}")
        except AttributeError: pass

    def xoa_ket_qua(self):
        try:
            self.lbl_chi_phi.configure(text="Chi phí: -")
            self.lbl_lo_trinh.configure(text="Lộ trình: -")
        except AttributeError: pass
    
    #endregion