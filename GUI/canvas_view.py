import tkinter as tk
import copy
from tkinter import messagebox, filedialog
import customtkinter as ctk
import GUI.canvas_function as cf

class Canvas(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.mode = "normal"
        self.node_count = 0
        self.danh_sach_canh = []
        self.history = []
        self.selected_node = None

        self.configure(fg_color="white", bg_color="#6a76b5", corner_radius=25)
        self.configure(border_width=3, border_color="#000000")

        self.drawing_area = tk.Canvas(self, bg="white", highlightthickness=0, cursor="arrow")
        self.drawing_area.pack(fill="both", expand=True, padx=20, pady=20)

        #region event chuột
        self.drawing_area.bind("<Button-1>", self.on_canvas_click)
        self.drawing_area.bind("<B1-Motion>", self.on_mouse_move)
        self.drawing_area.bind("<ButtonRelease-1>", self.on_mouse_up)

        #endregion

    #region MODE
    def set_mode_them_dinh(self):
        self.mode = "add_node"
        self.drawing_area.config(cursor="cross")

    def set_mode_chon_tu_dinh(self, callback_ham):
        self.mode = "select_source"
        self.callback_chon_dinh = callback_ham
        self.drawing_area.config(cursor="hand2")

    def set_mode_chon_den_dinh(self, callback_ham):
        self.mode = "select_target"
        self.callback_chon_dinh = callback_ham
        self.drawing_area.config(cursor="hand2")

    def set_mode_di_chuyen(self):
        self.mode = "move_node"
        self.drawing_area.config(cursor="fleur")
        self.dragging_node = None
        self._drag_offset = (0, 0)

    def set_mode_normal(self):
        self.mode = "normal"
        self.drawing_area.config(cursor="arrow")
        self.dragging_node = None
        self._drag_offset = (0, 0)

    #endregion

    #region click chuột
    def on_canvas_click(self, event):
        if self.mode == "add_node":
            self.luu_lich_su()

            mouse_x = event.x
            mouse_y = event.y
            node_name = chr(65 + self.node_count) 
            cf.tao_dinh(self.drawing_area, mouse_x, mouse_y, node_name)
            self.node_count += 1
            return

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
                self.mode = "normal"
                self.drawing_area.config(cursor="arrow")
                self.callback_chon_dinh = None
            return

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
        if self.mode != "move_node": return

        items = self.drawing_area.find_overlapping(event.x, event.y, event.x+1, event.y+1)
        node_clicked = None
        if items:
            tags = self.drawing_area.gettags(items[-1])
            for tag in tags:
                if tag not in ["node", "label", "current"]:
                    node_clicked = tag
                    break
        if node_clicked:
            self.luu_lich_su()

            self.dragging_node = node_clicked
            center = self.get_node_center(node_clicked)
            if center:
                cx, cy = center
                self._drag_offset = (cx - event.x, cy - event.y)

    def on_mouse_move(self, event):
        if self.mode != "move_node" or not getattr(self, 'dragging_node', None): return
        node_name = self.dragging_node
        offset_x, offset_y = self._drag_offset
        new_cx = event.x + offset_x
        new_cy = event.y + offset_y

        items = self.drawing_area.find_withtag(node_name)
        for item in items:
            if self.drawing_area.type(item) == "oval":
                x1, y1, x2, y2 = self.drawing_area.coords(item)
                radius_x = (x2 - x1) / 2
                radius_y = (y2 - y1) / 2
                self.drawing_area.coords(item, new_cx - radius_x, new_cy - radius_y, new_cx + radius_x, new_cy + radius_y)
            elif self.drawing_area.type(item) == "text":
                self.drawing_area.coords(item, new_cx, new_cy)
        self.redraw_edges()

    def on_mouse_up(self, event):
        if self.mode != "move_node": return
        if getattr(self, 'dragging_node', None):
            self.dragging_node = None
            self._drag_offset = (0, 0)
            self.redraw_edges()

    def redraw_edges(self):
        self.drawing_area.delete("edge")
        
        # Tạo tập hợp các cặp cạnh (u, v) để tra cứu nhanh
        existing_edges = set()
        for edge in self.danh_sach_canh:
            existing_edges.add((edge['source'], edge['target']))

        for edge in list(self.danh_sach_canh):
            src = edge.get("source")
            tgt = edge.get("target")
            w = edge.get("weight")
            
            src_center = self.get_node_center(src)
            tgt_center = self.get_node_center(tgt)
            
            if src_center and tgt_center:
                x1, y1 = src_center
                x2, y2 = tgt_center
                
                offset = 0
                if (tgt, src) in existing_edges and src != tgt:
                    offset = 15 # Offset khi có cạnh tồn tại

                cf.tao_duong_noi(self.drawing_area, x1, y1, x2, y2, w, src, tgt, offset=offset)
    
    #endregion

    #region Graph 
    def reset_canvas(self):
        cf.xoa_tat_ca(self.drawing_area)
        self.node_count = 0
        self.mode = "normal"
        self.danh_sach_canh = []
        self.history = []
        self.drawing_area.config(cursor="arrow")
        if hasattr(self, 'info_frame'): self.info_frame.destroy()

    def thuc_hien_noi_dinh(self, ten_dinh_1, ten_dinh_2, trong_so):
        self.danh_sach_canh.append({"source": ten_dinh_1, "target": ten_dinh_2, "weight": trong_so})
        self.redraw_edges() # Gọi redraw để offset

    def reset_mau_dinh(self, node_name):
        if node_name: cf.chinh_mau_dinh(self.drawing_area, node_name, "white")

    def highlight_duong_di(self, list_nodes):
        self.drawing_area.itemconfig("day_noi", fill="black", width=2)
        if len(list_nodes) < 2: return
        for i in range(len(list_nodes) - 1):
            u = list_nodes[i]
            v = list_nodes[i+1]
            tag_can_tim = f"edge_{u}_{v}"
            self.drawing_area.itemconfig(tag_can_tim, fill="red", width=4)

    def get_node_center(self, node_name):
        items = self.drawing_area.find_withtag(node_name)
        for item in items:
            if self.drawing_area.type(item) == "oval":
                coords = self.drawing_area.coords(item)
                return (coords[0] + coords[2])/2, (coords[1] + coords[3])/2

    def to_mau_dinh(self, node_name, color):
        if node_name: cf.chinh_mau_dinh(self.drawing_area, node_name, color)
    
    #endregion

    #region lưu/load dữ liệu file
    def luu_du_lieu(self):
        data = cf.lay_du_lieu_do_thi(self.drawing_area)
        data["edges"] = self.danh_sach_canh
        if cf.luu_file_txt(data, file_path="data_dothi.txt"):
            messagebox.showinfo("Thông báo", "Lưu file thành công!")
        else:
            messagebox.showerror("Lỗi", "Có lỗi xảy ra khi lưu file!")

    def export_data_text(self):
        data = cf.lay_du_lieu_do_thi(self.drawing_area)
        data["edges"] = self.danh_sach_canh
        lines = ["Vertex"]
        for node in data["nodes"]:
            lines.append(f"{node['id']} {node['x']} {node['y']}")
        lines.append("Edge")
        for edge in data["edges"]:
            lines.append(f"{edge['source']} {edge['target']} {edge['weight']}")
        return "\n".join(lines) + "\n"
    
    def load_du_lieu_tu_file(self):
        file_path = filedialog.askopenfilename(title="Chọn file dữ liệu đồ thị", filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
        if not file_path: return
        data = cf.doc_file_txt(file_path)
        if not data:
            messagebox.showerror("Lỗi", "Không đọc được file!")
            return
        self.reset_canvas()
        max_char_code = 64
        for node in data["nodes"]:
            cf.tao_dinh(self.drawing_area, node["x"], node["y"], node["id"])
            if len(node["id"]) == 1:
                code = ord(node["id"])
                if code > max_char_code: max_char_code = code
        self.node_count = (max_char_code - 64)
        for edge in data["edges"]:
            self.thuc_hien_noi_dinh(edge["source"], edge["target"], edge["weight"])
        messagebox.showinfo("Thành công", "Đã tải dữ liệu xong!")
    
    #endregion

    #region INFO BOX
    def hien_thi_bang_thong_tin(self, so_dinh, so_canh, danh_sach_canh, tong_trong_so):
        if hasattr(self, 'info_frame') and self.info_frame:
            self.info_frame.destroy()

        self.info_frame = ctk.CTkFrame(self, fg_color="white", border_width=2, border_color="#2C3E50", corner_radius=10, width=200)
        self.info_frame.place(relx=1.0, rely=1.0, anchor="se", x=-30, y=-30)

        header_frame = ctk.CTkFrame(self.info_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=10, pady=(5, 0))

        ctk.CTkLabel(header_frame, text="Thông tin Đồ thị", font=("Montserrat", 12, "bold"), text_color="#2C3E50").pack(side="left")
        
        ctk.CTkButton(
            header_frame, text="✕", width=20, height=20, fg_color="transparent", 
            text_color="red", hover_color="#FDEDEC", command=self.an_bang_thong_tin
        ).pack(side="right")

        content = f"• Số đỉnh: {so_dinh}\n• Số cạnh: {so_canh}\n• Tổng giá trị: {tong_trong_so}"
        ctk.CTkLabel(self.info_frame, text=content, justify="left", anchor="w", font=("Montserrat", 11), text_color="black").pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(self.info_frame, text="Danh sách cạnh:", font=("Montserrat", 11, "bold"), text_color="#2C3E50", anchor="w").pack(fill="x", padx=10, pady=(5, 0))

        scroll_frame = ctk.CTkScrollableFrame(self.info_frame, height=100, width=180, fg_color="#F4F6F7")
        scroll_frame.pack(padx=10, pady=(0, 10))

        if not danh_sach_canh:
            ctk.CTkLabel(scroll_frame, text="(Trống)", font=("Montserrat", 10), text_color="grey").pack()
        else:
            for canh in danh_sach_canh:
                text_canh = f"{canh['source']} -> {canh['target']}: {canh['weight']}"
                ctk.CTkLabel(
                    scroll_frame, text=text_canh, 
                    font=("Montserrat", 11), text_color="black", anchor="w",
                    height=20 
                ).pack(fill="x", pady=0) 

    def an_bang_thong_tin(self):
        if hasattr(self, 'info_frame') and self.info_frame:
            self.info_frame.destroy()
    
    #endregion

    #region lịch sử
    def luu_lich_su(self):
        current_data = cf.lay_du_lieu_do_thi(self.drawing_area)
        
        # Tạo snapshot (Bản chụp)
        state = {
            "nodes": current_data["nodes"],
            "edges": copy.deepcopy(self.danh_sach_canh),
            "node_count": self.node_count
        }
        
        self.history.append(state)
        # Giới hạn lịch sử
        if len(self.history) > 20:
            self.history.pop(0)

    def thuc_hien_undo(self):
        if not self.history:
            messagebox.showinfo("Thông báo", "Không còn gì để Undo!")
            return

        # Lấy trạng thái gần nhất
        last_state = self.history.pop()
        
        # Khôi phục dữ liệu
        self.reset_canvas_for_undo() # Hàm reset nhưng không xóa history
        self.node_count = last_state["node_count"]
        self.danh_sach_canh = last_state["edges"]

        # Vẽ lại đỉnh
        for node in last_state["nodes"]:
            cf.tao_dinh(self.drawing_area, node["x"], node["y"], node["id"])
        
        # Vẽ lại cạnh
        self.redraw_edges()

    def reset_canvas_for_undo(self):
        """Reset canvas nhưng giữ lại history"""
        cf.xoa_tat_ca(self.drawing_area)
        # Không reset self.history ở đây
        if hasattr(self, 'info_frame'): self.info_frame.destroy()

    #endregion
