import math

def tao_dinh(canvas_widget, x, y, label_text, radius=20):
    """ Hàm tạo 1 đỉnh """
    # Tính toán tọa độ hình chữ nhật bao quanh hình tròn
    x0 = x - radius
    y0 = y - radius
    x1 = x + radius
    y1 = y + radius

    # Vẽ hình tròn (Node)
    node_id = canvas_widget.create_oval(
        x0, y0, x1, y1,
        outline="#3B8ED0",  # Màu viền xanh (giống nút bấm)
        fill="white",       # Nền trắng
        width=2,
        tags=("node", label_text) # Gán tag để sau này dễ xóa hoặc di chuyển
    )

    # Vẽ chữ nằm chính giữa
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

def tao_duong_noi(canvas_widget, x1, y1, x2, y2, trong_so, name1, name2, radius=20):
    """Vẽ đường nối và đặt tag định danh (ví dụ: edge_A_B)"""
    # Tính toán khoảng cách (giữ nguyên)
    dx = x2 - x1
    dy = y2 - y1
    length = math.sqrt(dx**2 + dy**2)
    if length == 0: return

    # Tính điểm đầu cuối (giữ nguyên)
    start_x = x1 + (dx / length) * radius
    start_y = y1 + (dy / length) * radius
    end_x = x2 - (dx / length) * radius
    end_y = y2 - (dy / length) * radius

    # Tạo tag định danh duy nhất
    tag_id = f"edge_{name1}_{name2}" 

    # Vẽ đường thẳng (Cập nhật phần tags)
    canvas_widget.create_line(
        start_x, start_y, end_x, end_y,
        arrow="last",
        width=2,
        fill="black",
        arrowshape=(12, 15, 5),
        tags=("edge", "day_noi", tag_id)
    )

    # Vẽ số trọng số (giữ nguyên, nhưng thêm tag_id để xóa nếu cần)
    mid_x = (x1 + x2) / 2
    mid_y = (y1 + y2) / 2
    
    canvas_widget.create_rectangle(
        mid_x - 10, mid_y - 10, mid_x + 10, mid_y + 10,
        fill="white", 
        outline="", 
        tags="edge"
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
    
    # Lấy dữ liệu ĐỈNH
    all_items = canvas_widget.find_all()
    for item in all_items:
        tags = canvas_widget.gettags(item)
        
        if "node" in tags:
            # Lấy tên đỉnh (là tag không phải "node" hay "current")
            node_name = [t for t in tags if t not in ["node", "current"]][0]
            
            # Lấy tọa độ để xác định vị trí
            x1, y1, x2, y2 = canvas_widget.coords(item)
            center_x = (x1 + x2) / 2
            center_y = (y1 + y2) / 2
            
            data["nodes"].append({
                "id": node_name,
                "x": center_x,
                "y": center_y
            })
    
    return data

def luu_file_txt(data, file_path="data_dothi.txt"):
    """Ghi dữ liệu xuống file txt"""
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("Vertex\n") # Ghi đỉnh
        for node in data["nodes"]:
            line = f"{node['id']} {node['x']} {node['y']}\n"
            f.write(line)
        
        f.write("Edge\n") # Ghi cạnh
        for edge in data["edges"]:
            line = f"{edge['source']} {edge['target']} {edge['weight']}\n"
            f.write(line)

    return True

def xoa_tat_ca(canvas_widget):
    canvas_widget.delete("all")
