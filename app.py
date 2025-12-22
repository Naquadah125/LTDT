from tkinter import messagebox
import customtkinter as ctk
from GUI.canvas_view import Canvas
from GUI.sidebar_view import Sidebar
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
        
        self.sidebar_frame.btn_load_file.configure(
            command=self.map_frame.load_du_lieu_tu_file
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
        
        self.sidebar_frame.btn_reset_algo.configure(
            command=self.xu_ly_lam_moi_thuat_toan
        )
        
        #endregion
        
    def xu_ly_them_canh(self):
        # Lấy dữ liệu từ Sidebar
        u = self.sidebar_frame.tu_dinh_da_chon
        v = self.sidebar_frame.den_dinh_da_chon
        w = self.sidebar_frame.entry_trong_so.get()

        # Kiểm tra dữ liệu hợp lệ
        if u is None or v is None:
            return
        if not w: 
            w = "0" # Mặc định là 0
        
        # Xử lý trùng lặp cạnh
        for edge in self.map_frame.danh_sach_canh:
            if edge['source'] == u and edge['target'] == v:
                messagebox.showwarning(
                    "Trùng lặp", 
                    f"Cạnh từ {u} đến {v} đã tồn tại!"
                )
                return

        # Gửi sang Canvas để vẽ
        self.map_frame.thuc_hien_noi_dinh(u, v, w)

        # Reset form
        self.map_frame.reset_mau_dinh(u)
        self.map_frame.reset_mau_dinh(v)
        self.sidebar_frame.reset_form_nhap_lieu()

    def xu_ly_chay_thuat_toan(self):
        graph_text = self.map_frame.export_data_text()

        # lấy start và end của khu vực thuật toán
        start = self.sidebar_frame.algo_start_node
        end = self.sidebar_frame.algo_end_node
        algo_name = self.sidebar_frame.option_thuat_toan.get()

        if algo_name == "Dijkstra":
            if not start or not end:
                messagebox.showwarning("Thiếu thông tin", "Vui lòng chọn đầy đủ:\n- Điểm Bắt đầu\n- Điểm Kết thúc")
                return
            
        elif algo_name == "Traveling Salesman":
            if not start:
                messagebox.showwarning("Thiếu thông tin", "Vui lòng chọn Điểm Bắt đầu!")
                return

        if start: # remove color highlight cũ
            self.map_frame.reset_mau_dinh(start)
        if end:
            self.map_frame.reset_mau_dinh(end)

        if algo_name == "Dijkstra":
            # Gọi hàm backend dijkstra
            success, data = bc.goi_backend_dijkstra(start, end, graph_text)
            
            if success:
                chi_phi, path_nodes = data
                messagebox.showinfo("Kết quả", f"Chi phí: {chi_phi}\nLộ trình: {' -> '.join(path_nodes)}")
                self.map_frame.highlight_duong_di(path_nodes)# Vẽ highlight bên canvas
            else:
                messagebox.showerror("Lỗi", data)
        
        elif algo_name == "Traveling Salesman":
            # Gọi backend TSP
            success, data = bc.goi_backend_tsp(start, graph_text)

            if success:
                chi_phi, path_nodes = data
                
                messagebox.showinfo("Kết quả TSP", f"Tổng chi phí: {chi_phi}\nLộ trình: {' -> '.join(path_nodes)}")
                self.map_frame.highlight_duong_di(path_nodes)# vẽ highlight bên canvas
            else:
                messagebox.showerror("Lỗi TSP", data)

        else:
            messagebox.showinfo("Thông báo", "Chức năng này chưa phát triển xong.")

    def xu_ly_lam_moi_thuat_toan(self):
        """Xử lý khi bấm nút Refresh (↻)"""
        
        # Xóa đường màu đỏ trên bản đồ
        self.map_frame.highlight_duong_di([]) 

        # Trả lại màu trắng cho các đỉnh đang được chọn (nếu có)
        start = self.sidebar_frame.algo_start_node
        end = self.sidebar_frame.algo_end_node
        if start: 
            self.map_frame.reset_mau_dinh(start)
        if end: 
            self.map_frame.reset_mau_dinh(end)

        # Reset giao diện bên Sidebar
        self.sidebar_frame.reset_algo_ui()
        
if __name__ == "__main__":
    app = App()
    app.mainloop()