import json
import math

def tao_dinh(canvas_widget, x, y, label_text, radius=20):
    """ Hàm tạo 1 đỉnh """
    
    # 1. Tính toán tọa độ hình chữ nhật bao quanh hình tròn
    x0 = x - radius
    y0 = y - radius
    x1 = x + radius
    y1 = y + radius

    # 2. Vẽ hình tròn (Node)
    node_id = canvas_widget.create_oval(
        x0, y0, x1, y1,
        outline="#3B8ED0",  # Màu viền xanh (giống nút bấm)
        fill="white",       # Nền trắng
        width=2,
        tags=("node", label_text) # Gán tag để sau này dễ xóa hoặc di chuyển
    )

    # 3. Vẽ chữ nằm chính giữa
    text_id = canvas_widget.create_text(
        x, y,
        text=label_text,
        font=("Montserrat", 12, "bold"), # Dùng font hệ thống hoặc font bạn đã nạp
        fill="black",
        tags=("label", label_text)
    )

    return node_id, text_id

def chinh_mau_dinh(canvas_widget, node_name, color):
    """
    Đổi màu nền của đỉnh có tên node_name (A, B, C...) thành màu color.
    Chỉ đổi màu hình tròn (oval), không đổi màu chữ.
    """
    # Lấy danh sách các vật thể có tag là tên đỉnh (gồm cả hình tròn và chữ)
    items = canvas_widget.find_withtag(node_name)
    
    for item in items:
        # Kiểm tra xem vật thể này có phải hình tròn không (type='oval')
        if canvas_widget.type(item) == "oval":
            canvas_widget.itemconfig(item, fill=color)

def tao_duong_noi(canvas_widget, x1, y1, x2, y2, trong_so, radius=20):
    """Vẽ đường nối từ viền hình tròn này sang viền hình tròn kia"""
    
    # 1. Tính khoảng cách giữa 2 tâm
    dx = x2 - x1
    dy = y2 - y1
    length = math.sqrt(dx**2 + dy**2)

    # Nếu 2 điểm quá gần (trùng nhau), không vẽ để tránh lỗi chia cho 0
    if length == 0: return

    # 2. Tính tọa độ điểm bắt đầu (trên viền node 1)
    # Công thức: x_new = x1 + (dx / length) * radius
    start_x = x1 + (dx / length) * radius
    start_y = y1 + (dy / length) * radius

    # 3. Tính tọa độ điểm kết thúc (trên viền node 2)
    # Chúng ta lùi lại từ đích một khoảng radius
    end_x = x2 - (dx / length) * radius
    end_y = y2 - (dy / length) * radius

    # 4. Vẽ đường thẳng (Dùng tọa độ mới: start -> end)
    canvas_widget.create_line(
        start_x, start_y, end_x, end_y,
        arrow="last",
        width=2,
        fill="black",
        arrowshape=(12, 15, 5),
        tags="edge"
    )

    # 5. Vẽ số trọng số ở trung điểm (giữ nguyên logic cũ)
    mid_x = (x1 + x2) / 2
    mid_y = (y1 + y2) / 2
    
    canvas_widget.create_rectangle(
        mid_x - 10, mid_y - 10, mid_x + 10, mid_y + 10,
        fill="white", outline="", tags="edge"
    )
    
    canvas_widget.create_text(
        mid_x, mid_y,
        text=str(trong_so),
        fill="red",
        font=("Arial", 12, "bold"),
        tags="edge"
    )

def lay_du_lieu_do_thi(canvas_widget):
    """Quét canvas và trả về dictionary chứa nodes và edges"""
    data = {
        "nodes": [],
        "edges": []
    }
    
    # Lấy dữ liệu ĐỈNH (Nodes)
    all_items = canvas_widget.find_all()
    for item in all_items:
        tags = canvas_widget.gettags(item)
        
        # Nếu là node (hình tròn)
        if "node" in tags:
            # Lấy tên đỉnh (là tag không phải "node" hay "current")
            node_name = [t for t in tags if t not in ["node", "current"]][0]
            
            # Lấy tọa độ tâm
            x1, y1, x2, y2 = canvas_widget.coords(item)
            center_x = (x1 + x2) / 2
            center_y = (y1 + y2) / 2
            
            data["nodes"].append({
                "id": node_name,
                "x": center_x,
                "y": center_y
            })
    
    return data

def luu_file_json(data, file_path="data_dothi.json"):
    """Ghi dữ liệu xuống file"""
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"--> Đã lưu file thành công: {file_path}")
        return True
    except Exception as e:
        print(f"--> Lỗi lưu file: {e}")
        return False

def xoa_tat_ca(canvas_widget):
    canvas_widget.delete("all")