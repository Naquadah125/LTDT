import subprocess
import os
import tempfile

def goi_backend_dijkstra(start_node, end_node, graph_text=None):
    """Gọi backend từ backend.exe trong thư mục Backend (cố định)."""
    project_backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Backend'))
    backend_path = os.path.join(project_backend_dir, 'backend.exe' if os.name == 'nt' else 'backend')
    temp_path = None
    try:
        if graph_text is not None:
            tf = tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w", encoding="utf-8")
            tf.write(graph_text)
            tf.flush()
            tf.close()
            temp_path = tf.name
            data_arg = temp_path
        else:
            data_arg = "data_dothi.txt"

        startupinfo = None
        if os.name == 'nt':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        completed = subprocess.run([backend_path, "DIJKSTRA", start_node, end_node, data_arg],
                                   check=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   text=True,
                                   startupinfo=startupinfo)

        out = completed.stdout.strip()
        if not out:
            return False, "Backend không trả kết quả!"

        lines = out.splitlines()
        line1 = lines[0].strip()

        if line1 == "Khong Thay Duong":
            return False, "Không tìm thấy đường đi!"
        elif line1.startswith("Loi"):
            return False, f"Backend báo: {line1}"

        chi_phi = line1
        path_nodes = lines[1].strip().split() if len(lines) > 1 else []
        return True, (chi_phi, path_nodes)

    except subprocess.CalledProcessError as e:
        stderr = e.stderr.strip() if hasattr(e, 'stderr') and e.stderr else str(e)
        return False, f"Lỗi chạy backend: {stderr}"
    except Exception as e:
        return False, f"Lỗi backend: {e}"
    finally:
        if temp_path:
            try:
                os.remove(temp_path)
            except:
                pass
