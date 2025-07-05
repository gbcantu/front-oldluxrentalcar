import tkinter as tk
from tkinter import ttk, messagebox

def carregar(container):
    style = ttk.Style()
    style.configure('TFrame', background='#f0f2f5')
    style.configure('TLabel', background='#f0f2f5', font=('Segoe UI', 10))
    style.configure('TButton', font=('Segoe UI', 10), padding=5)
    style.configure('TEntry', fieldbackground='white', background='white')
    style.configure('TLabelframe', background='#f0f2f5', borderwidth=1, relief='solid')
    style.configure('TLabelframe.Label', background='#f0f2f5', font=('Segoe UI', 10, 'bold'))
    style.map('TButton', background=[('active', '#4472C4')], foreground=[('active', 'white')])

    canvas = tk.Canvas(container, bg='#f0f2f5', highlightthickness=0)
    scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
    
    main_frame = ttk.Frame(canvas, style='TFrame')
    
    main_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )
    
    canvas.create_window((0, 0), window=main_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    title_frame = ttk.Frame(main_frame, style='TFrame')
    title_frame.pack(fill='x', pady=(0, 20), padx=20)
    
    ttk.Label(title_frame, 
             text="Configurações do Sistema", 
             font=('Segoe UI', 14, 'bold'), 
             foreground='#2b579a', 
             style='TLabel').pack(side='left')
    
    ttk.Label(main_frame, 
             text="Configure as preferências do sistema Old&Lux Rental Car", 
             font=('Segoe UI', 9), 
             foreground='#666666', 
             style='TLabel').pack(fill='x', pady=(0, 20), padx=20)

    # Seção Configurações Gerais
    config_frame = ttk.LabelFrame(main_frame, 
                                text="Configurações Gerais",
                                padding=(15, 10),
                                style='TLabelframe')
    config_frame.pack(fill='x', pady=(0, 25), padx=20)
    
    ttk.Label(config_frame, text="Preferências do Sistema", style='TLabel').pack(anchor='w', pady=(0, 10))

    form_frame = ttk.Frame(config_frame, style='TFrame')
    form_frame.pack(fill='x')

    ttk.Label(form_frame, text="Tema da Interface:", style='TLabel').grid(row=0, column=0, sticky='e', padx=5, pady=5)
    combo_tema = ttk.Combobox(form_frame, values=["Claro", "Escuro", "Sistema"], width=15, state="readonly")
    combo_tema.set("Claro")
    combo_tema.grid(row=0, column=1, sticky='w', padx=5, pady=5)

    ttk.Label(form_frame, text="Idioma:", style='TLabel').grid(row=0, column=2, sticky='e', padx=(15,5), pady=5)
    combo_idioma = ttk.Combobox(form_frame, values=["Português", "Inglês", "Espanhol"], width=15, state="readonly")
    combo_idioma.set("Português")
    combo_idioma.grid(row=0, column=3, sticky='w', padx=5, pady=5)

    ttk.Label(form_frame, text="Formato de Data:", style='TLabel').grid(row=1, column=0, sticky='e', padx=5, pady=5)
    combo_data = ttk.Combobox(form_frame, values=["DD/MM/AAAA", "MM/DD/AAAA", "AAAA-MM-DD"], width=15, state="readonly")
    combo_data.set("DD/MM/AAAA")
    combo_data.grid(row=1, column=1, sticky='w', padx=5, pady=5)

    ttk.Label(form_frame, text="Moeda:", style='TLabel').grid(row=1, column=2, sticky='e', padx=(15,5), pady=5)
    combo_moeda = ttk.Combobox(form_frame, values=["Real (R$)", "Dólar (US$)", "Euro (€)"], width=15, state="readonly")
    combo_moeda.set("Real (R$)")
    combo_moeda.grid(row=1, column=3, sticky='w', padx=5, pady=5)

    btn_frame = ttk.Frame(config_frame, style='TFrame')
    btn_frame.pack(fill='x', pady=(10, 0))
    
    btn_salvar = ttk.Button(btn_frame, 
                          text="Salvar Configurações", 
                          style='Accent.TButton')
    btn_salvar.pack(side='left', padx=5)

    # Seção Sobre o Sistema
    sobre_frame = ttk.LabelFrame(main_frame, 
                               text="Sobre o Sistema", 
                               padding=(15, 10),
                               style='TLabelframe')
    sobre_frame.pack(fill='x', pady=(0, 15), padx=20)
    
    ttk.Label(sobre_frame, text="Informações do Sistema", style='TLabel').pack(anchor='w', pady=(0, 10))

    sobre_form_frame = ttk.Frame(sobre_frame, style='TFrame')
    sobre_form_frame.pack(fill='x')

    sobre_texto = """Sistema de Gestão - Old&Lux Rental Car

Desenvolvido por:
Gabriel Cantú - Analista de T.I.

Versão: 1.0.0
Última atualização: Junho/2025"""

    ttk.Label(sobre_form_frame, 
             text=sobre_texto,
             justify='left',
             style='TLabel').grid(row=0, column=0, sticky='w', padx=5, pady=5, columnspan=4)

    button_frame = ttk.Frame(sobre_frame, style='TFrame')
    button_frame.pack(fill='x', pady=(15, 5))

    btn_atualizar = ttk.Button(button_frame, text="Verificar Atualizações")
    btn_atualizar.pack(side='left', padx=5)

    btn_licenca = ttk.Button(button_frame, text="Termos de Licença")
    btn_licenca.pack(side='left', padx=5)

    btn_suporte = ttk.Button(button_frame, text="Suporte Técnico")
    btn_suporte.pack(side='left', padx=5)

    style.configure('Accent.TButton', foreground='white', background='#2b579a')
    style.configure('Danger.TButton', foreground='white', background='#d83b01')

    return main_frame