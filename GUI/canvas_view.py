import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import GUI.canvas_function as cf

class Canvas(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.mode = "normal"  # Các mode: "normal", "add_node"
        self.node_count = 0   # Đếm số đỉnh để đặt tên A, B, C...

        self.danh_sach_canh = []
        self.selected_node = None

        # Border edge
        self.configure(
            fg_color="white",
            bg_color="#6a76b5",
            corner_radius=25
        )

        # Border
        self.configure(
            border_width=3,
            border_color="#000000"
        )

        self.drawing_area = tk.Canvas(
            self, 
            bg="white", 
            highlightthickness=0,
            cursor="arrow"
        )
        self.drawing_area.pack(fill="both", expand=True, padx=20, pady=20)

        self.drawing_area.bind("<Button-1>", self.on_canvas_click)

    #region MODE
    def set_mode_them_dinh(self):
        """Chuyển sang chế độ thêm đỉnh"""
        self.mode = "add_node"
        self.drawing_area.config(cursor="cross") # Đổi con trỏ thành hình dấu cộng

    def set_mode_chon_tu_dinh(self, callback_ham):
        """Chuyển mode và ghi nhớ hàm cần gọi lại"""
        self.mode = "select_source"
        self.callback_chon_dinh = callback_ham # Lưu hàm lại để dùng sau
        self.drawing_area.config(cursor="hand2")

    def set_mode_chon_den_dinh(self, callback_ham):
        """Chuyển mode và ghi nhớ hàm cần gọi lại"""
        self.mode = "select_target"
        self.callback_chon_dinh = callback_ham # Lưu hàm lại
        self.drawing_area.config(cursor="hand2")

    #endregion

    def on_canvas_click(self, event):
        """Xử lý khi người dùng bấm chuột vào canvas"""
        if self.mode == "add_node":
            # 1. Lấy tọa độ chuột
            mouse_x = event.x
            mouse_y = event.y
            
            # 2. Tạo tên đỉnh tự động (A, B, C...)
            node_name = chr(65 + self.node_count) # ASCII: 65='A', 66='B'...
            cf.tao_dinh(self.drawing_area, mouse_x, mouse_y, node_name)
            
            # 3. Cập nhật trạng thái
            self.node_count += 1

        if self.mode in ["select_source", "select_target"]:
            # 1. Tìm đỉnh tại vị trí click
            items = self.drawing_area.find_overlapping(event.x, event.y, event.x+1, event.y+1)
            
            node_clicked = None
            if items:
                tags = self.drawing_area.gettags(items[-1])
                for tag in tags:
                    if tag not in ["node", "label", "current"]:
                        node_clicked = tag
                        break
            
            if node_clicked:
                # 2. Highlight đỉnh vừa chọn (Màu xanh lá mạ chẳng hạn)
                cf.chinh_mau_dinh(self.drawing_area, node_clicked, "#AED6F1")

                # 3. GỌI CALLBACK ĐỂ BÁO VỀ SIDEBAR
                if self.callback_chon_dinh:
                    self.callback_chon_dinh(node_clicked)

                # 4. Reset về chế độ bình thường sau khi chọn xong
                self.mode = "normal"
                self.drawing_area.config(cursor="arrow")
                self.callback_chon_dinh = None # Xóa nhiệm vụ

    def reset_canvas(self):
        """Xóa sạch và reset bộ đếm"""
        # 1. Xóa giao diện
        cf.xoa_tat_ca(self.drawing_area)
        
        # 2. Reset dữ liệu logic
        self.node_count = 0
        self.mode = "normal"
        self.danh_sach_canh = []
        
        # 3. Reset con trỏ chuột
        self.drawing_area.config(cursor="arrow")
    
    def thuc_hien_noi_dinh(self, ten_dinh_1, ten_dinh_2, trong_so):
        """Tìm tọa độ 2 đỉnh và vẽ đường nối"""
        
        # 1. Hàm con để lấy tọa độ tâm của một đỉnh theo tên (Tag)
        def lay_toa_do_tam(ten_tag):
            # Tìm tất cả vật thể có tag tên đỉnh (gồm hình tròn + chữ)
            items = self.drawing_area.find_withtag(ten_tag)
            for item in items:
                # Chỉ lấy tọa độ của hình tròn (oval)
                if self.drawing_area.type(item) == "oval":
                    x1, y1, x2, y2 = self.drawing_area.coords(item)
                    center_x = (x1 + x2) / 2
                    center_y = (y1 + y2) / 2
                    return center_x, center_y
            return None, None

        # 2. Lấy tọa độ thật của 2 đỉnh
        x_start, y_start = lay_toa_do_tam(ten_dinh_1)
        x_end, y_end = lay_toa_do_tam(ten_dinh_2)

        # 3. Nếu tìm thấy cả 2 thì gọi hàm vẽ bên cf
        if x_start is not None and x_end is not None:
            cf.tao_duong_noi(
                self.drawing_area, 
                x_start, y_start, 
                x_end, y_end, 
                trong_so
            )

            self.danh_sach_canh.append({
                "source": ten_dinh_1,
                "target": ten_dinh_2,
                "weight": trong_so
            })
        else:
            print("--> Lỗi: Không tìm thấy đỉnh trên canvas!")

    def reset_mau_dinh(self, node_name):
        """Tô lại màu trắng cho đỉnh"""
        if node_name:
            cf.chinh_mau_dinh(self.drawing_area, node_name, "white")

    def luu_du_lieu(self):
        # Lấy thông tin vertex và edges
        data = cf.lay_du_lieu_do_thi(self.drawing_area)
        data["edges"] = self.danh_sach_canh
        
        # Lưu 
        ket_qua = cf.luu_file_txt(data, file_path="data_dothi.txt")

        # Hiển thị menu 'thành công'
        if ket_qua == True:
            messagebox.showinfo("Thông báo", "Lưu file thành công!")
        else:
            messagebox.showerror("Lỗi", "Có lỗi xảy ra khi lưu file!")

            