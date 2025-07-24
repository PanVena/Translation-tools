import os
import sys
import tkinter as tk
from tkinter import messagebox
import pandas as pd
from PIL import Image

def resource_path(relative_path):
    """Повертає шлях до ресурсу, враховуючи запуск з .exe (PyInstaller)"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# === Шляхи ===
GLYPHS_IMAGE_PATH = resource_path("font_regular.png")
GLYPHS_TABLE_PATH = resource_path("glyphs_font_regular.csv")
OUTPUT_DIR = os.path.abspath(".")

# === Завантаження таблиці і зображення ===
glyphs_table = pd.read_csv(GLYPHS_TABLE_PATH, sep=';', skiprows=1, header=None)
glyphs_table.columns = ['code', 'x', 'y', 'width', 'height', 'col6', 'col7']
glyphs_image = Image.open(GLYPHS_IMAGE_PATH).convert("RGBA")

def get_glyph(char):
    code = ord(char)
    row = glyphs_table[glyphs_table['code'] == code]
    if row.empty:
        return None
    x, y, w, h = row.iloc[0][['x', 'y', 'width', 'height']]
    glyph = glyphs_image.crop((x, y, x + w, y + h))
    return glyph

def render_text(text, spacing=1):
    glyphs = [get_glyph(char) for char in text]
    glyphs = [g for g in glyphs if g is not None]
    
    if not glyphs:
        raise ValueError("No valid glyphs found for input text.")
    
    total_width = sum(g.width + spacing for g in glyphs) - spacing
    max_height = max(g.height for g in glyphs)
    
    img = Image.new("RGBA", (total_width, max_height), (0, 0, 0, 0))
    x_offset = 0
    for g in glyphs:
        img.paste(g, (x_offset, 0), g)
        x_offset += g.width + spacing
    
    return img

def render_and_save():
    text = entry.get().strip()
    if not text:
        messagebox.showwarning("Помилка", "Введіть текст.")
        return
    try:
        img = render_text(text)
        output_path = os.path.join(OUTPUT_DIR, f"{text}.png")
        img.save(output_path)
        messagebox.showinfo("Успіх", f"Зображення збережено як:\n{output_path}")
    except Exception as e:
        messagebox.showerror("Помилка", str(e))

# === GUI ===
root = tk.Tk()
root.title("Текст → PNG")
root.geometry("300x150")
root.resizable(False, False)

tk.Label(root, text="Введіть текст:").pack(pady=10)
entry = tk.Entry(root, width=30)
entry.pack()

tk.Button(root, text="Створити PNG", command=render_and_save).pack(pady=10)

root.mainloop()

