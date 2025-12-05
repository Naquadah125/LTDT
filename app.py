import tkinter as tk
import customtkinter as ctk
import GUI.canvas_function as cf
from GUI.canvas_view import Canvas
from GUI.sidebar_view import Sidebar

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Ứng dụng Tìm đường Du lịch")
        self.geometry("1200x800")

        self.configure(fg_color="#6a76b5")
        self.columnconfigure(0, weight=9)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        # Load canvas
        self.map_frame = Canvas(self)
        self.map_frame.grid(
            row=0, column=0, 
            sticky="nsew", 
            padx=(20, 10),  # Cách lề trái 20px, cách lề phải 10px (để tạo khe giữa)
            pady=20         # Cách trên dưới 20px
        )

        # Load sidebar
        self.sidebar_frame = Sidebar(self)
        self.sidebar_frame.grid(
            row=0, column=1, 
            sticky="nsew", 
            padx=(0, 20),   # Không cách trái (để dính vào khe giữa), cách phải 20px
            pady=20         # Cách trên dưới 20px
        )

        #region MODE Button
        self.sidebar_frame.btn_them_dinh.configure(
            command=self.map_frame.set_mode_them_dinh
        )

        self.sidebar_frame.btn_xoa_dinh.configure(
            command=self.map_frame.reset_canvas
        )

        self.sidebar_frame.btn_tu_dinh.configure(
            command=lambda: self.map_frame.set_mode_chon_tu_dinh(
                self.sidebar_frame.cap_nhat_nut_tu_dinh
            )
        )
        
        self.sidebar_frame.btn_den_dinh.configure(
            command=lambda: self.map_frame.set_mode_chon_den_dinh(
                self.sidebar_frame.cap_nhat_nut_den_dinh
            )
        )

        self.sidebar_frame.btn_them_canh.configure(
            command=self.xu_ly_them_canh
        )

        self.sidebar_frame.btn_luu_file.configure(
            command=self.map_frame.luu_du_lieu
        )
        #endregion
        
    def xu_ly_them_canh(self):
        # 1. Lấy dữ liệu từ Sidebar
        u = self.sidebar_frame.tu_dinh_da_chon
        v = self.sidebar_frame.den_dinh_da_chon
        w = self.sidebar_frame.entry_trong_so.get()

        # 2. Kiểm tra dữ liệu hợp lệ
        if u is None or v is None:
            return
        
        if not w: 
            w = "0" # Mặc định là 0 nếu không nhập
        
        # 3. Gửi sang Canvas để vẽ
        self.map_frame.thuc_hien_noi_dinh(u, v, w)

        # 4. Reset form
        self.map_frame.reset_mau_dinh(u) # Trả A về màu trắng
        self.map_frame.reset_mau_dinh(v) # Trả B về màu trắng
        self.sidebar_frame.reset_form_nhap_lieu()

if __name__ == "__main__":
    app = App()
    app.mainloop()