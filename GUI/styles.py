import os
from customtkinter import FontManager

FONT_FAMILY = "Montserrat"

def load_custom_font():
    # Tìm đường dẫn file font
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    font_path = os.path.join(project_root, "fonts", "Montserrat-VariableFont_wght.ttf")

    # Load font
    try:
        FontManager.load_font(font_path)
        return True
    except Exception as e:
        print(f"Something went wrong: {e}")
        return False

def get_font(size=14, weight="normal"):
    return (FONT_FAMILY, size, weight)