import tkinter as tk
from tkinter import messagebox, filedialog
import customtkinter as ctk
import GUI.canvas_function as cf

class Canvas(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.mode = "normal"  # Các mode "normal", "add_node",... 
        self.node_count = 0

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

        #rengion event chuột
        self.drawing_area.bind("<Button-1>", self.on_canvas_click)
        self.drawing_area.bind("<B1-Motion>", self.on_mouse_move)
        self.drawing_area.bind("<ButtonRelease-1>", self.on_mouse_up)

        #endregion

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

    def set_mode_di_chuyen(self):
        """Chuyển sang chế độ di chuyển đỉnh (bấm giữ + kéo)"""
        self.mode = "move_node"
        self.drawing_area.config(cursor="fleur")
        self.dragging_node = None
        self._drag_offset = (0, 0)

    def set_mode_normal(self):
        """Quay về chế độ bình thường"""
        self.mode = "normal"
        self.drawing_area.config(cursor="arrow")
        self.dragging_node = None
        self._drag_offset = (0, 0)

    #endregion

    #region click chuột
    def on_canvas_click(self, event):
        """Hàm xử lý duy nhất khi bấm chuột trái"""
        # TRƯỜNG HỢP 1: THÊM ĐỈNH (Add Node)
        if self.mode == "add_node":
            mouse_x = event.x
            mouse_y = event.y
            
            # Tạo tên đỉnh (A, B, C...)
            node_name = chr(65 + self.node_count) 
            cf.tao_dinh(self.drawing_area, mouse_x, mouse_y, node_name)
            self.node_count += 1
            return # Quan trọng: return để dừng, không chạy code bên dưới

        # TRƯỜNG HỢP 2: CHỌN ĐỈNH (Select Source/Target)
        if self.mode in ["select_source", "select_target"]:
            items = self.drawing_area.find_overlapping(event.x, event.y, event.x+1, event.y+1)
            
            node_clicked = None
            if items:
                tags = self.drawing_area.gettags(items[-1])
                for tag in tags:
                    if tag not in ["node", "label", "current"]:
                        node_clicked = tag
                        break
            
            if node_clicked:
                cf.chinh_mau_dinh(self.drawing_area, node_clicked, "#AED6F1")
                if self.callback_chon_dinh:
                    self.callback_chon_dinh(node_clicked)

                # Reset về chế độ bình thường sau khi chọn xong
                self.mode = "normal"
                self.drawing_area.config(cursor="arrow")
                self.callback_chon_dinh = None
            return

        # TRƯỜNG HỢP 3: DI CHUYỂN ĐỈNH
        if self.mode == "move_node":
            items = self.drawing_area.find_overlapping(event.x, event.y, event.x+1, event.y+1)
            node_clicked = None
            if items:
                tags = self.drawing_area.gettags(items[-1])
                for tag in tags:
                    if tag not in ["node", "label", "current"]:
                        node_clicked = tag
                        break

            if node_clicked:
                self.dragging_node = node_clicked
                center = self.get_node_center(node_clicked)
                if center:
                    cx, cy = center
                    self._drag_offset = (cx - event.x, cy - event.y)

    #endregion

    #region kéo di chuyển đỉnh
    def on_mouse_down(self, event):
        """Bắt đầu kéo đỉnh nếu đang ở chế độ di chuyển"""
        if self.mode != "move_node":
            return

        items = self.drawing_area.find_overlapping(event.x, event.y, event.x+1, event.y+1)
        node_clicked = None
        if items:
            tags = self.drawing_area.gettags(items[-1])
            for tag in tags:
                if tag not in ["node", "label", "current"]:
                    node_clicked = tag
                    break

        if node_clicked:
            self.dragging_node = node_clicked
            center = self.get_node_center(node_clicked)
            if center:
                cx, cy = center
                self._drag_offset = (cx - event.x, cy - event.y)

    def on_mouse_move(self, event):
        """Di chuyển đỉnh khi giữ chuột"""
        if self.mode != "move_node" or not getattr(self, 'dragging_node', None):
            return

        node_name = self.dragging_node
        # Tính tọa độ mới của tâm
        offset_x, offset_y = self._drag_offset
        new_cx = event.x + offset_x
        new_cy = event.y + offset_y

        # Tìm các items thuộc node và cập nhật tọa độ
        items = self.drawing_area.find_withtag(node_name)
        for item in items:
            if self.drawing_area.type(item) == "oval":
                # lấy bán kính
                x1, y1, x2, y2 = self.drawing_area.coords(item)
                radius_x = (x2 - x1) / 2
                radius_y = (y2 - y1) / 2
                x0 = new_cx - radius_x
                y0 = new_cy - radius_y
                x1 = new_cx + radius_x
                y1 = new_cy + radius_y
                self.drawing_area.coords(item, x0, y0, x1, y1)
            elif self.drawing_area.type(item) == "text":
                self.drawing_area.coords(item, new_cx, new_cy)
        self.redraw_edges()

    def on_mouse_up(self, event):
        """Kết thúc kéo, reset trạng thái drag"""
        if self.mode != "move_node":
            return

        if getattr(self, 'dragging_node', None):
            self.dragging_node = None
            self._drag_offset = (0, 0)
            self.redraw_edges()

    def redraw_edges(self):
        """Xóa và vẽ lại toàn bộ cạnh ứng với vị trí đỉnh hiện tại"""
        self.drawing_area.delete("edge")

        # Vẽ lại từng cạn
        for edge in list(self.danh_sach_canh):
            src = edge.get("source")
            tgt = edge.get("target")
            w = edge.get("weight")
            src_center = self.get_node_center(src)
            tgt_center = self.get_node_center(tgt)
            if src_center and tgt_center:
                x1, y1 = src_center
                x2, y2 = tgt_center
                cf.tao_duong_noi(self.drawing_area, x1, y1, x2, y2, w, src, tgt)

    #endregion

    #region Graph 
    def reset_canvas(self):
        """Xóa sạch và reset bộ đếm"""
        cf.xoa_tat_ca(self.drawing_area)
        
        self.node_count = 0
        self.mode = "normal"
        self.danh_sach_canh = []
        
        self.drawing_area.config(cursor="arrow")
    
    def thuc_hien_noi_dinh(self, ten_dinh_1, ten_dinh_2, trong_so):
        """Tìm tọa độ 2 đỉnh và vẽ đường nối"""
        # magic
        def lay_toa_do_tam(ten_tag):
            items = self.drawing_area.find_withtag(ten_tag)
            for item in items:
                # Chỉ lấy tọa độ của hình tròn (oval)
                if self.drawing_area.type(item) == "oval":
                    x1, y1, x2, y2 = self.drawing_area.coords(item)
                    center_x = (x1 + x2) / 2
                    center_y = (y1 + y2) / 2
                    return center_x, center_y
            return None, None

        x_start, y_start = lay_toa_do_tam(ten_dinh_1)
        x_end, y_end = lay_toa_do_tam(ten_dinh_2)
        if x_start is not None and x_end is not None:
            cf.tao_duong_noi(
                self.drawing_area, 
                x_start, y_start, 
                x_end, y_end, 
                trong_so,
                ten_dinh_1,
                ten_dinh_2
            )

            self.danh_sach_canh.append({
                "source": ten_dinh_1,
                "target": ten_dinh_2,
                "weight": trong_so
            })
        else:
            print("Không tìm thấy đỉnh")

    def reset_mau_dinh(self, node_name):
        """Tô lại màu trắng cho đỉnh"""
        if node_name:
            cf.chinh_mau_dinh(self.drawing_area, node_name, "white")

    def highlight_duong_di(self, list_nodes):
        """Đổi màu các cạnh có sẵn sang màu đỏ"""
        self.drawing_area.itemconfig("day_noi", fill="black", width=2)

        if len(list_nodes) < 2: return

        # Duyệt qua lộ trình và đổi màu từng cạnh cụ thể
        for i in range(len(list_nodes) - 1):
            u = list_nodes[i]
            v = list_nodes[i+1]
            
            # Tìm cạnh cần tô màu lại
            tag_can_tim = f"edge_{u}_{v}"
            self.drawing_area.itemconfig(
                tag_can_tim, 
                fill="red",
                width=4
            )

    def get_node_center(self, node_name):
        """Hàm phụ tìm tọa độ tâm hình tròn dựa trên tên đỉnh"""
        items = self.drawing_area.find_withtag(node_name)
        
        for item in items:
            if self.drawing_area.type(item) == "oval":
                coords = self.drawing_area.coords(item)
                return (coords[0] + coords[2])/2, (coords[1] + coords[3])/2
    
    def to_mau_dinh(self, node_name, color):
        """Hàm wrapper để tô màu đỉnh tùy ý"""
        if node_name:
            cf.chinh_mau_dinh(self.drawing_area, node_name, color)
    #endregion

    #region lưu/load dữ liệu file
    def luu_du_lieu(self):
        # Lấy thông tin vertex và edges
        data = cf.lay_du_lieu_do_thi(self.drawing_area)
        data["edges"] = self.danh_sach_canh
    
        ket_qua = cf.luu_file_txt(data, file_path="data_dothi.txt")

        # Hiển thị menu 'thành công'
        if ket_qua == True:
            messagebox.showinfo("Thông báo", "Lưu file thành công!")
        else:
            messagebox.showerror("Lỗi", "Có lỗi xảy ra khi lưu file!")

    def export_data_text(self):
        """Trả về nội dung file data_dothi.txt hiện tại dưới dạng chuỗi (không ghi ra đĩa)."""
        data = cf.lay_du_lieu_do_thi(self.drawing_area) # Lấy thông tin vertex và edges
        data["edges"] = self.danh_sach_canh

        # Tạo chuỗi định dạng file txt
        lines = ["Vertex"]
        for node in data["nodes"]:
            lines.append(f"{node['id']} {node['x']} {node['y']}")
        lines.append("Edge")
        for edge in data["edges"]:
            lines.append(f"{edge['source']} {edge['target']} {edge['weight']}")
        return "\n".join(lines) + "\n"
    
    def load_du_lieu_tu_file(self):
        """Mở hộp thoại chọn file và load dữ liệu từ file vào canvas"""
        
        # Mở hộp thoại chọn file
        file_path = filedialog.askopenfilename(
            title="Chọn file dữ liệu đồ thị",
            filetypes=(("Text Files", "*.txt"), ("All Files", "*.*"))
        )
        
        if not file_path: return # Người dùng bấm hủy thì thoát

        # Gọi hàm đọc file bên canvas_function
        data = cf.doc_file_txt(file_path)
        if not data:
            messagebox.showerror("Lỗi", "Không đọc được file hoặc định dạng sai!")
            return

        self.reset_canvas()

        # Vẽ lại đỉnh
        max_char_code = 64
        for node in data["nodes"]:
            # Vẽ đỉnh lên màn hình
            cf.tao_dinh(self.drawing_area, node["x"], node["y"], node["id"])
            
            if len(node["id"]) == 1: 
                code = ord(node["id"])
                if code > max_char_code:
                    max_char_code = code
        self.node_count = (max_char_code - 64)

        # Vẽ lại cạnh
        for edge in data["edges"]:
            self.thuc_hien_noi_dinh(
                edge["source"], 
                edge["target"], 
                edge["weight"]
            )

        messagebox.showinfo("Thành công", "Đã tải dữ liệu xong!")

    #endregion

