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
            command=self.on_click_them_dinh
        )

        self.sidebar_frame.btn_xoa_dinh.configure(
            command=lambda: [self.reset_nut_di_chuyen(), self.map_frame.reset_canvas()]
        )

        self.sidebar_frame.btn_tu_dinh.configure(
            command=self.on_click_tu_dinh
        )
        
        self.sidebar_frame.btn_den_dinh.configure(
            command=self.on_click_den_dinh
        )

        self.sidebar_frame.btn_reset_ket_noi.configure(
            command=self.xu_ly_lam_moi_ket_noi
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
            command=self.on_click_algo_start
        )

        self.sidebar_frame.btn_end_node.configure(
            command=self.on_click_algo_end
        )

        self.sidebar_frame.btn_run_algorithm.configure(
            command=self.xu_ly_chay_thuat_toan
        )
        
        self.sidebar_frame.btn_reset_algo.configure(
            command=self.xu_ly_lam_moi_thuat_toan
        )

        self.sidebar_frame.btn_move_node.configure(
            command=self.toggle_move_mode
        )
        
        #endregion
        
    #region Xử lý functions
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

    def xu_ly_lam_moi_ket_noi(self):
        """Xử lý khi bấm Refresh ở phần Kết nối đỉnh:
        - Xóa highlight (nếu có) của các đỉnh đang chọn
        - Reset form nhập cạnh trong Sidebar
        """
        u = self.sidebar_frame.tu_dinh_da_chon
        v = self.sidebar_frame.den_dinh_da_chon
        if u:
            self.map_frame.reset_mau_dinh(u)
        if v:
            self.map_frame.reset_mau_dinh(v)

        # Reset form bên Sidebar
        self.sidebar_frame.reset_form_nhap_lieu()

    def toggle_move_mode(self):
        """Bật/tắt chế độ di chuyển đỉnh từ nút sidebar"""
        if getattr(self.map_frame, 'mode', 'normal') != 'move_node':
            # Bật chế độ di chuyển
            self.map_frame.set_mode_di_chuyen()
            self.sidebar_frame.btn_move_node.configure(text="Ngừng ", fg_color="#000000")
        else:
            # Tắt chế độ di chuyển
            self.map_frame.set_mode_normal()
            self.sidebar_frame.btn_move_node.configure(text="Di chuyển", fg_color="#9B9B9B")

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
                # Hiển thị kết quả trong Sidebar thay vì popup
                self.sidebar_frame.hien_thi_ket_qua(chi_phi, path_nodes, algo_name="Dijkstra")
                self.map_frame.highlight_duong_di(path_nodes) # Vẽ highlight bên canvas
            else:
                messagebox.showerror("Lỗi", data)
        
        elif algo_name == "Traveling Salesman":
            # Gọi backend TSP
            success, data = bc.goi_backend_tsp(start, graph_text)

            if success:
                chi_phi, path_nodes = data
                self.sidebar_frame.hien_thi_ket_qua(chi_phi, path_nodes, algo_name="Traveling Salesman")
                self.map_frame.highlight_duong_di(path_nodes) # vẽ highlight bên canvas
            else:
                messagebox.showerror("Lỗi TSP", data)

        else:
            messagebox.showinfo("Thông báo", "Chức năng này chưa phát triển xong.")

    def xu_ly_lam_moi_thuat_toan(self):
        """Xử lý khi bấm nút Refresh (↻)"""
        self.map_frame.highlight_duong_di([]) 

        start = self.sidebar_frame.algo_start_node
        end = self.sidebar_frame.algo_end_node
        if start: 
            self.map_frame.reset_mau_dinh(start)
        if end: 
            self.map_frame.reset_mau_dinh(end)

        # Reset giao diện bên Sidebar
        self.sidebar_frame.reset_algo_ui()
        self.sidebar_frame.xoa_ket_qua()
    
    def xu_ly_chon_start(self, ten_dinh_moi):
        """Callback khi người dùng chọn xong điểm Bắt đầu trên Canvas"""
        dinh_cu = self.sidebar_frame.algo_start_node
        if dinh_cu and dinh_cu != ten_dinh_moi:
            self.map_frame.reset_mau_dinh(dinh_cu)
            
        # Cập nhật Sidebar
        self.sidebar_frame.cap_nhat_algo_start(ten_dinh_moi)
        self.map_frame.to_mau_dinh(ten_dinh_moi, "#AED6F1")

    def xu_ly_chon_end(self, ten_dinh_moi):
        """Callback khi người dùng chọn xong điểm Kết thúc"""
        dinh_cu = self.sidebar_frame.algo_end_node
        if dinh_cu and dinh_cu != ten_dinh_moi:
            self.map_frame.reset_mau_dinh(dinh_cu)
            
        # Cập nhật Sidebar
        self.sidebar_frame.cap_nhat_algo_end(ten_dinh_moi)
        self.map_frame.to_mau_dinh(ten_dinh_moi, "#AED6F1")

    def reset_nut_di_chuyen(self):
        """Đưa nút di chuyển và chế độ di chuyển về trạng thái tắt"""
        self.sidebar_frame.btn_move_node.configure(
            text="Di chuyển", 
            fg_color="#9B9B9B"
        )
        
        if self.map_frame.mode == "move_node":
            self.map_frame.set_mode_normal()
    #endregion

    #region wrapper cho event click chuột
    def on_click_them_dinh(self):
        self.reset_nut_di_chuyen() # Tắt chế độ di chuyển trước
        self.map_frame.set_mode_them_dinh() # Sau đó mới chuyển sang thêm đỉnh

    def on_click_tu_dinh(self):
        self.reset_nut_di_chuyen()
        self.map_frame.set_mode_chon_tu_dinh(
            self.sidebar_frame.cap_nhat_nut_tu_dinh
        )

    def on_click_den_dinh(self):
        self.reset_nut_di_chuyen()
        self.map_frame.set_mode_chon_den_dinh(
            self.sidebar_frame.cap_nhat_nut_den_dinh
        )

    def on_click_algo_start(self):
        self.reset_nut_di_chuyen()
        self.map_frame.set_mode_chon_tu_dinh(
            self.xu_ly_chon_start
        )

    def on_click_algo_end(self):
        self.reset_nut_di_chuyen()
        self.map_frame.set_mode_chon_den_dinh(
            self.xu_ly_chon_end
        )

    #endregion

if __name__ == "__main__":
    app = App()
    app.mainloop()