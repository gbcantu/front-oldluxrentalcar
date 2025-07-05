import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
from PIL import Image, ImageTk
import os

def carregar(container):
    frame = tk.Frame(container, bg='#f8f9fa')
    frame.pack(fill='both', expand=True)
    
    header_frame = tk.Frame(frame, bg='#343a40', height=100)
    header_frame.pack(fill='x')
    header_frame.pack_propagate(False)

    tk.Label(
        header_frame,
        text="Old&Lux Rental Car",
        font=('Segoe UI', 24, 'bold'),
        fg='white',
        bg='#343a40'
    ).pack(side='left', padx=10)
    
    content_frame = tk.Frame(frame, bg='#f8f9fa', padx=20, pady=20)
    content_frame.pack(fill='both', expand=True)
    
    cards_frame = tk.Frame(content_frame, bg='#f8f9fa')
    cards_frame.pack(fill='x', pady=(0, 30))
    
    card1 = tk.Frame(cards_frame, bg='white', padx=20, pady=15, relief='groove', bd=1)
    card1.pack(side='left', expand=True, fill='both', padx=5)
    
    tk.Label(
        card1,
        text="Faturamento Mensal",
        font=('Segoe UI', 12, 'bold'),
        bg='white'
    ).pack(anchor='w')
    
    card1.lbl_value = tk.Label(
        card1,
        text="Carregando...",
        font=('Segoe UI', 24),
        bg='white'
    )
    card1.lbl_value.pack(pady=5)
    
    card2 = tk.Frame(cards_frame, bg='white', padx=20, pady=15, relief='groove', bd=1)
    card2.pack(side='left', expand=True, fill='both', padx=5)
    
    tk.Label(
        card2,
        text="Veículos Disponíveis",
        font=('Segoe UI', 12, 'bold'),
        bg='white'
    ).pack(anchor='w')
    
    card2.lbl_value = tk.Label(
        card2,
        text="Carregando...",
        font=('Segoe UI', 24),
        bg='white'
    )
    card2.lbl_value.pack(pady=5)
    
    nav_frame = tk.Frame(content_frame, bg='#f8f9fa')
    nav_frame.pack(fill='both', expand=True)
    
    tk.Label(
        nav_frame,
        text="Acesso Rápido",
        font=('Segoe UI', 16, 'bold'),
        bg='#f8f9fa'
    ).pack(anchor='w', pady=(0, 15))
    
    buttons_grid = tk.Frame(nav_frame, bg='#f8f9fa')
    buttons_grid.pack(fill='both', expand=True)
    
    buttons_config = [
        ("Clientes", "#007bff", "clientes", "clientes.png"),
        ("Veículos", "#28a745", "veiculos", "veiculos.png"), 
        ("Agendamentos", "#6f42c1", "agendamentos", "agendamentos.png"),
        ("Documentos", "#fd7e14", "documentos", "documentos.png"),
        ("Manutenções", "#dc3545", "manutencoes", "manutencao.png"),
        ("Configurações", "#6c757d", "configuracoes", "config.png")
    ]
    
    for i, (text, color, view, icon_file) in enumerate(buttons_config):
        row = i // 3
        col = i % 3
        
        try:
            icon_path = os.path.join("assets", icon_file)
            icon_img = Image.open(icon_path)
            icon_img = icon_img.resize((40, 40), Image.Resampling.LANCZOS)
            icon_photo = ImageTk.PhotoImage(icon_img)
            
            btn = tk.Button(
                buttons_grid,
                text=text,
                image=icon_photo,
                compound='top',
                font=('Segoe UI', 12, 'bold'),
                bg='white',
                fg=color,
                activebackground='#e9ecef',
                activeforeground=color,
                relief='flat',
                bd=2,
                padx=20,
                pady=15,
                command=lambda v=view: navegar_para_view(v)
            )
            btn.image = icon_photo
            btn.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
            
            buttons_grid.rowconfigure(row, weight=1)
            buttons_grid.columnconfigure(col, weight=1)
        except Exception as e:
            print(f"Erro ao criar botão {text}: {e}")

    footer_frame = tk.Frame(frame, bg='#343a40', height=40)
    footer_frame.pack(fill='x', side='bottom')
    footer_frame.pack_propagate(False)
    
    tk.Label(
        footer_frame,
        text="© 2025 Old&Lux Rental Car - Sistema de Gestão",
        font=('Segoe UI', 8),
        fg='white',
        bg='#343a40'
    ).pack(side='right', padx=20)

def navegar_para_view(view_name):
    print(f"Navegando para: {view_name}")

def atualizar_dados(faturamento, veiculos_disponiveis):
    for widget in globals():
        if hasattr(widget, 'lbl_value'):
            if "Faturamento" in widget.winfo_children()[0].cget("text"):
                widget.lbl_value.config(text=f"R$ {faturamento:,.2f}")
            elif "Veículos" in widget.winfo_children()[0].cget("text"):
                widget.lbl_value.config(text=str(veiculos_disponiveis))
