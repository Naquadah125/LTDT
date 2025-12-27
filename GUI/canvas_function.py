import math
from . import styles

def tao_dinh(canvas_widget, x, y, label_text, radius=20):
    x0, y0, x1, y1 = x - radius, y - radius, x + radius, y + radius
    
    node_id = canvas_widget.create_oval(
        x0, y0, x1, y1,
        outline="#3B8ED0", fill="white", width=2,
        tags=("node", label_text)
    )
    text_id = canvas_widget.create_text(
        x, y, text=label_text, font=("Montserrat", 12, "bold"), fill="black",
        tags=("label", label_text)
    )
    return node_id, text_id

def chinh_mau_dinh(canvas_widget, node_name, color):
    items = canvas_widget.find_withtag(node_name)
    for item in items:
        if canvas_widget.type(item) == "oval":
            canvas_widget.itemconfig(item, fill=color)

def tao_duong_noi(canvas_widget, x1, y1, x2, y2, trong_so, name1, name2, radius=20, offset=0):
    tag_id = f"edge_{name1}_{name2}" 

    # 1. CẠNH KHUYÊN
    if name1 == name2:
        start_x, start_y = x1 - 10, y1 - radius
        end_x, end_y = x1 + 10, y1 - radius
        cp1_x, cp1_y = x1 - 30, y1 - 50
        cp2_x, cp2_y = x1 + 30, y1 - 50

        canvas_widget.create_line(
            start_x, start_y, cp1_x, cp1_y, cp2_x, cp2_y, end_x, end_y,
            smooth=True, arrow="last", width=2, fill="black", arrowshape=(12, 15, 5),
            tags=("edge", "day_noi", tag_id)
        )
        mid_x, mid_y = x1, y1 - 50
        canvas_widget.create_rectangle(mid_x-10, mid_y-10, mid_x+10, mid_y+10, fill="white", outline="", tags="edge")
        canvas_widget.create_text(mid_x, mid_y, text=str(trong_so), fill="red", font=styles.get_font(size=12, weight="bold"), tags="edge")
        return

    # 2. CẠNH THƯỜNG
    dx = x2 - x1
    dy = y2 - y1
    length = math.sqrt(dx**2 + dy**2)
    if length == 0: return

    ux, uy = dx / length, dy / length
    nx, ny = -uy, ux

    shift_x = nx * offset
    shift_y = ny * offset

    real_x1 = x1 + shift_x
    real_y1 = y1 + shift_y
    real_x2 = x2 + shift_x
    real_y2 = y2 + shift_y

    if radius > abs(offset):
        dist_to_edge = math.sqrt(radius**2 - offset**2)
    else:
        dist_to_edge = 0 
    
    start_x = real_x1 + ux * dist_to_edge
    start_y = real_y1 + uy * dist_to_edge
    end_x = real_x2 - ux * dist_to_edge
    end_y = real_y2 - uy * dist_to_edge

    canvas_widget.create_line(
        start_x, start_y, end_x, end_y,
        arrow="last", width=2, fill="black", arrowshape=(12, 15, 5),
        tags=("edge", "day_noi", tag_id)
    )

    mid_x = (start_x + end_x) / 2
    mid_y = (start_y + end_y) / 2
    
    canvas_widget.create_rectangle(mid_x-10, mid_y-10, mid_x+10, mid_y+10, fill="white", outline="", tags="edge")
    canvas_widget.create_text(mid_x, mid_y, text=str(trong_so), fill="red", font=styles.get_font(size=12, weight="bold"), tags="edge")

def lay_du_lieu_do_thi(canvas_widget):
    data = {"nodes": [], "edges": []}
    all_items = canvas_widget.find_all()
    for item in all_items:
        tags = canvas_widget.gettags(item)
        if "node" in tags:
            node_name = [t for t in tags if t not in ["node", "current"]][0]
            x1, y1, x2, y2 = canvas_widget.coords(item)
            data["nodes"].append({"id": node_name, "x": (x1 + x2)/2, "y": (y1 + y2)/2})
    return data

def luu_file_txt(data, file_path="data_dothi.txt"):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("Vertex\n")
        for node in data["nodes"]: f.write(f"{node['id']} {node['x']} {node['y']}\n")
        f.write("Edge\n")
        for edge in data["edges"]: f.write(f"{edge['source']} {edge['target']} {edge['weight']}\n")
    return True

def xoa_tat_ca(canvas_widget):
    canvas_widget.delete("all")

def doc_file_txt(file_path):
    data = {"nodes": [], "edges": []}
    try:
        with open(file_path, "r", encoding="utf-8") as f: lines = f.readlines()
        mode = ""
        for line in lines:
            parts = line.strip().split()
            if not parts: continue
            if parts[0] in ["Vertex", "*NODES"]: mode = "Vertex"; continue
            elif parts[0] in ["Edge", "*EDGES"]: mode = "Edge"; continue
            
            if mode == "Vertex" and len(parts) >= 3:
                data["nodes"].append({"id": parts[0], "x": float(parts[1]), "y": float(parts[2])})
            elif mode == "Edge" and len(parts) >= 3:
                data["edges"].append({"source": parts[0], "target": parts[1], "weight": parts[2]})
        return data
    except Exception: return None
