import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import GUI.canvas_function as cf
from GUI.canvas_view import Canvas
from GUI.sidebar_view import Sidebar
import GUI.sidebar_function as sf
import Backend.backend_client as bc

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

        #region Button
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
        
        self.sidebar_frame.btn_start_node.configure(
            command=lambda: self.map_frame.set_mode_chon_tu_dinh(
                self.sidebar_frame.cap_nhat_algo_start
            )
        )

        self.sidebar_frame.btn_end_node.configure(
            command=lambda: self.map_frame.set_mode_chon_den_dinh(
                self.sidebar_frame.cap_nhat_algo_end
            )
        )

        self.sidebar_frame.btn_run_algorithm.configure(
            command=self.xu_ly_chay_thuat_toan
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

    def xu_ly_chay_thuat_toan(self):
        graph_text = self.map_frame.export_data_text()

        # lấy start và end của khu vực thuật toán
        start = self.sidebar_frame.algo_start_node
        end = self.sidebar_frame.algo_end_node
        algo_name = self.sidebar_frame.option_thuat_toan.get()

        if start: # remove color highlight cũ
            self.map_frame.reset_mau_dinh(start)
        if end:
            self.map_frame.reset_mau_dinh(end)

        if algo_name == "Dijkstra":
            # Gọi hàm backend
            success, data = bc.goi_backend_dijkstra(start, end, graph_text)
            
            if success:
                chi_phi, path_nodes = data
                messagebox.showinfo("Kết quả", f"Chi phí: {chi_phi}\nLộ trình: {' -> '.join(path_nodes)}")
                self.map_frame.highlight_duong_di(path_nodes)      # Vẽ highlight bên canvas
            else:
                messagebox.showerror("Lỗi", data)
        
        else:
            messagebox.showinfo("Thông báo", "Chức năng này chưa phát triển xong.")

if __name__ == "__main__":
    app = App()
    app.mainloop()