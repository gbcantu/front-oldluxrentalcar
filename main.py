import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from PIL import Image, ImageTk
import os
import sys

from views import (
    home_view,
    clientes_view,
    veiculos_view,
    agendamentos_view,
    documentos_view,
    manutencao_view,
    config_view
)

class OldLuxApp:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.create_sidebar()
        self.create_main_area()
        self.navegar_para_view("home")
    
    def setup_window(self):
        self.root.title("Old&Lux Rental Car - Sistema de Gestão")
        self.root.geometry("1200x700")
        self.root.minsize(1000, 700)
        self.root.configure(bg='#f8f9fa')
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TButton', font=('Segoe UI', 10))
        self.style.configure('TEntry', padding=5)
        
    def create_sidebar(self):
        self.sidebar = tk.Frame(self.root, bg='#343a40', width=220)
        self.sidebar.pack(side='left', fill='y')
        self.sidebar.pack_propagate(False)
        
        logo_frame = tk.Frame(self.sidebar, bg='#343a40', height=120)
        logo_frame.pack(fill='x', pady=(10, 20))
        logo_frame.pack_propagate(False)
        
        logo_img = self.load_image("logo.png", (150, 150))
        logo_label = tk.Label(logo_frame, image=logo_img, bg='#343a40')
        logo_label.image = logo_img
        logo_label.pack(pady=10)
        
        nav_buttons = [
            ("home.png", "Home", "home"),
            ("clientes.png", "Clientes", "clientes"),
            ("veiculos.png", "Veículos", "veiculos"),
            ("agendamentos.png", "Agendamentos", "agendamentos"),
            ("documentos.png", "Documentos", "documentos"),
            ("manutencao.png", "Manutenções", "manutencoes")
        ]
        
        for icon, text, view in nav_buttons:
            self.create_nav_button(icon, text, view)
        
        tk.Frame(self.sidebar, bg='#495057', height=2).pack(fill='x', pady=10)
        
        self.create_nav_button("config.png", "Configurações", "configuracoes")
        
        version_frame = tk.Frame(self.sidebar, bg='#343a40')
        version_frame.pack(side='bottom', fill='x', pady=10)
        tk.Label(
            version_frame,
            text="v1.0.0",
            font=('Segoe UI', 8),
            fg='#adb5bd',
            bg='#343a40'
        ).pack(side='right', padx=10)
    
    def create_nav_button(self, icon, text, view):
        btn_frame = tk.Frame(self.sidebar, bg='#343a40')
        btn_frame.pack(fill='x', padx=10, pady=2)
        
        icon_img = self.load_image(icon, (20, 20))
        
        btn = tk.Button(
            btn_frame,
            text=f"  {text}",
            image=icon_img,
            compound='left',
            font=('Segoe UI', 11),
            fg='white',
            bg='#343a40',
            activeforeground='white',
            activebackground='#495057',
            relief='flat',
            anchor='w',
            padx=10,
            command=lambda: self.navegar_para_view(view)
        )
        btn.image = icon_img
        btn.pack(fill='x')
        
        btn.bind("<Enter>", lambda e: btn.config(bg='#495057'))
        btn.bind("<Leave>", lambda e: btn.config(bg='#343a40'))
    
    def create_main_area(self):
        self.main_area = tk.Frame(self.root, bg='#f8f9fa')
        self.main_area.pack(side='right', expand=True, fill='both')
    
    def load_image(self, filename, size=None):
        try:
            path = os.path.join("assets", filename)
            img = Image.open(path)
            if size:
                img = img.resize(size, Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Error loading image {filename}: {str(e)}")
            return ImageTk.PhotoImage(Image.new('RGBA', size or (24, 24), (0,0,0,0)))
    
    def navegar_para_view(self, view_name):
        views = {
            'home': home_view,
            'clientes': clientes_view,
            'veiculos': veiculos_view,
            'agendamentos': agendamentos_view,
            'documentos': documentos_view,
            'manutencoes': manutencao_view,
            'configuracoes': config_view
        }
        
        if view_name in views:
            for widget in self.main_area.winfo_children():
                widget.destroy()
            views[view_name].carregar(self.main_area)
            if hasattr(views[view_name], 'navegar_para_view'):
                views[view_name].navegar_para_view = self.navegar_para_view

def main():
    root = ThemedTk(theme="arc")
    try:
        icon_path = os.path.join("assets", "logo.ico")
        root.iconbitmap(icon_path)
    except:
        pass
    app = OldLuxApp(root)
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    root.mainloop()

if __name__ == '__main__':
    main()
