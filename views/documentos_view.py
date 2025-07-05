import tkinter as tk
from tkinter import ttk, messagebox
import requests
from datetime import datetime

BASE_URL = "http://localhost:8000"

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
             text="Gerenciamento de Documentos de Veículos", 
             font=('Segoe UI', 14, 'bold'), 
             foreground='#2b579a', 
             style='TLabel').pack(side='left')
    
    ttk.Label(main_frame, 
             text="Cadastre, edite e consulte os documentos dos veículos da Old&Lux Rental Car", 
             font=('Segoe UI', 9), 
             foreground='#666666', 
             style='TLabel').pack(fill='x', pady=(0, 20), padx=20)

    add_frame = ttk.LabelFrame(main_frame, 
                              text="Novo Documento", 
                              padding=(15, 10),
                              style='TLabelframe')
    add_frame.pack(fill='x', pady=(0, 25), padx=20)
    
    ttk.Label(add_frame, text="Dados do Documento", style='TLabel').pack(anchor='w', pady=(0, 10))

    form_frame = ttk.Frame(add_frame, style='TFrame')
    form_frame.pack(fill='x')

    ttk.Label(form_frame, text="ID Veículo:", style='TLabel').grid(row=0, column=0, sticky='e', padx=5, pady=5)
    entry_veiculo_id = ttk.Entry(form_frame, width=10, style='TEntry')
    entry_veiculo_id.grid(row=0, column=1, sticky='w', padx=5, pady=5)

    ttk.Label(form_frame, text="Tipo Documento:", style='TLabel').grid(row=0, column=2, sticky='e', padx=(15,5), pady=5)
    tipo_options = ["CRLV", "Seguro", "IPVA", "Licenciamento", "Outros"]
    combo_tipo = ttk.Combobox(form_frame, values=tipo_options, width=15, state="readonly")
    combo_tipo.grid(row=0, column=3, sticky='w', padx=5, pady=5)
    combo_tipo.set("CRLV")

    ttk.Label(form_frame, text="Número Documento:", style='TLabel').grid(row=1, column=0, sticky='e', padx=5, pady=5)
    entry_numero = ttk.Entry(form_frame, width=20, style='TEntry')
    entry_numero.grid(row=1, column=1, sticky='w', padx=5, pady=5, columnspan=3)

    ttk.Label(form_frame, text="Validade Início (AAAA-MM-DD):", style='TLabel').grid(row=2, column=0, sticky='e', padx=5, pady=5)
    entry_validade_inicio = ttk.Entry(form_frame, width=15, style='TEntry')
    entry_validade_inicio.grid(row=2, column=1, sticky='w', padx=5, pady=5)

    ttk.Label(form_frame, text="Validade Fim (AAAA-MM-DD):", style='TLabel').grid(row=2, column=2, sticky='e', padx=(15,5), pady=5)
    entry_validade_fim = ttk.Entry(form_frame, width=15, style='TEntry')
    entry_validade_fim.grid(row=2, column=3, sticky='w', padx=5, pady=5)

    ttk.Label(form_frame, text="Observações:", style='TLabel').grid(row=3, column=0, sticky='e', padx=5, pady=5)
    entry_observacoes = ttk.Entry(form_frame, width=50, style='TEntry')
    entry_observacoes.grid(row=3, column=1, sticky='w', padx=5, pady=5, columnspan=3)

    btn_frame = ttk.Frame(add_frame, style='TFrame')
    btn_frame.pack(fill='x', pady=(10, 0))
    
    btn_salvar = ttk.Button(btn_frame, 
                          text="Salvar", 
                          command=lambda: adicionar_documento(
                              entry_veiculo_id.get(),
                              combo_tipo.get(),
                              entry_numero.get(),
                              entry_validade_inicio.get(),
                              entry_validade_fim.get(),
                              entry_observacoes.get()
                          ), 
                          style='Accent.TButton')
    btn_salvar.pack(side='left', padx=5)

    edit_frame = ttk.LabelFrame(main_frame, 
                               text="Editar Documento", 
                               padding=(15, 10),
                               style='TLabelframe')
    edit_frame.pack(fill='x', pady=(0, 15), padx=20)
    
    ttk.Label(edit_frame, text="Dados do Documento", style='TLabel').pack(anchor='w', pady=(0, 10))

    edit_form_frame = ttk.Frame(edit_frame, style='TFrame')
    edit_form_frame.pack(fill='x')

    ttk.Label(edit_form_frame, text="ID Documento:", style='TLabel').grid(row=0, column=0, sticky='e', padx=5, pady=5)
    entry_id = ttk.Entry(edit_form_frame, width=10, style='TEntry')
    entry_id.grid(row=0, column=1, sticky='w', padx=5, pady=5)

    ttk.Label(edit_form_frame, text="ID Veículo:", style='TLabel').grid(row=1, column=0, sticky='e', padx=5, pady=5)
    entry_edit_veiculo_id = ttk.Entry(edit_form_frame, width=10, style='TEntry')
    entry_edit_veiculo_id.grid(row=1, column=1, sticky='w', padx=5, pady=5)

    ttk.Label(edit_form_frame, text="Tipo Documento:", style='TLabel').grid(row=1, column=2, sticky='e', padx=(15,5), pady=5)
    edit_tipo_options = ["CRLV", "Seguro", "IPVA", "Licenciamento", "Outros"]
    combo_edit_tipo = ttk.Combobox(edit_form_frame, values=edit_tipo_options, width=15, state="readonly")
    combo_edit_tipo.grid(row=1, column=3, sticky='w', padx=5, pady=5)

    ttk.Label(edit_form_frame, text="Número Documento:", style='TLabel').grid(row=2, column=0, sticky='e', padx=5, pady=5)
    entry_edit_numero = ttk.Entry(edit_form_frame, width=20, style='TEntry')
    entry_edit_numero.grid(row=2, column=1, sticky='w', padx=5, pady=5, columnspan=3)

    ttk.Label(edit_form_frame, text="Validade Início:", style='TLabel').grid(row=3, column=0, sticky='e', padx=5, pady=5)
    entry_edit_validade_inicio = ttk.Entry(edit_form_frame, width=15, style='TEntry')
    entry_edit_validade_inicio.grid(row=3, column=1, sticky='w', padx=5, pady=5)

    ttk.Label(edit_form_frame, text="Validade Fim:", style='TLabel').grid(row=3, column=2, sticky='e', padx=(15,5), pady=5)
    entry_edit_validade_fim = ttk.Entry(edit_form_frame, width=15, style='TEntry')
    entry_edit_validade_fim.grid(row=3, column=3, sticky='w', padx=5, pady=5)

    ttk.Label(edit_form_frame, text="Observações:", style='TLabel').grid(row=4, column=0, sticky='e', padx=5, pady=5)
    entry_edit_observacoes = ttk.Entry(edit_form_frame, width=50, style='TEntry')
    entry_edit_observacoes.grid(row=4, column=1, sticky='w', padx=5, pady=5, columnspan=3)

    button_frame = ttk.Frame(edit_frame, style='TFrame')
    button_frame.pack(fill='x', pady=(15, 5))

    btn_editar = ttk.Button(button_frame, 
                           text="Editar", 
                           command=lambda: editar_documento(
                               entry_id.get(),
                               entry_edit_veiculo_id.get(),
                               combo_edit_tipo.get(),
                               entry_edit_numero.get(),
                               entry_edit_validade_inicio.get(),
                               entry_edit_validade_fim.get(),
                               entry_edit_observacoes.get()
                           ))
    btn_editar.pack(side='left', padx=5)

    btn_excluir = ttk.Button(button_frame, 
                            text="Excluir", 
                            command=lambda: excluir_documento(entry_id.get()), 
                            style='Danger.TButton')
    btn_excluir.pack(side='left', padx=5)

    btn_buscar = ttk.Button(button_frame, 
                           text="Buscar", 
                           command=lambda: buscar_documento(
                               entry_id.get(),
                               entry_edit_veiculo_id,
                               combo_edit_tipo,
                               entry_edit_numero,
                               entry_edit_validade_inicio,
                               entry_edit_validade_fim,
                               entry_edit_observacoes
                           ))
    btn_buscar.pack(side='left', padx=5)

    btn_buscar_todos = ttk.Button(button_frame, 
                                 text="Buscar Todos", 
                                 command=buscar_todos_documentos)
    btn_buscar_todos.pack(side='left', padx=5)

    btn_buscar_veiculo = ttk.Button(button_frame, 
                                   text="Por Veículo", 
                                   command=lambda: buscar_documentos_por_veiculo(entry_edit_veiculo_id.get()))
    btn_buscar_veiculo.pack(side='left', padx=5)

    btn_limpar = ttk.Button(button_frame, 
                           text="Limpar", 
                           command=lambda: limpar_formulario(
                               entry_id,
                               entry_edit_veiculo_id,
                               combo_edit_tipo,
                               entry_edit_numero,
                               entry_edit_validade_inicio,
                               entry_edit_validade_fim,
                               entry_edit_observacoes,
                               entry_veiculo_id,
                               combo_tipo,
                               entry_numero,
                               entry_validade_inicio,
                               entry_validade_fim,
                               entry_observacoes
                           ))
    btn_limpar.pack(side='left', padx=5)

    style.configure('Accent.TButton', foreground='white', background='#2b579a')
    style.configure('Danger.TButton', foreground='white', background='#d83b01')

    return main_frame

def adicionar_documento(veiculo_id, tipo_documento, numero_documento, validade_inicio, validade_fim, observacoes):
    data = {
        "veiculo_id": int(veiculo_id) if veiculo_id else 0,
        "tipo_documento": tipo_documento,
        "numero_documento": numero_documento,
        "validade_inicio": validade_inicio,
        "validade_fim": validade_fim,
        "observacoes": observacoes
    }
    
    if not veiculo_id or not tipo_documento or not numero_documento:
        messagebox.showwarning("Aviso", "Veículo, Tipo e Número são obrigatórios!")
        return
    
    try:
        response = requests.post(f"{BASE_URL}/documentosveiculo/", json=data)
        if response.status_code == 201:
            messagebox.showinfo("Sucesso", "Documento cadastrado com sucesso!")
        else:
            messagebox.showerror("Erro", f"Erro ao cadastrar documento: {response.text}")
    except Exception as e:
        messagebox.showerror("Erro", f"Falha na comunicação com a API: {str(e)}")

def editar_documento(id, veiculo_id, tipo_documento, numero_documento, validade_inicio, validade_fim, observacoes):
    if not id:
        messagebox.showwarning("Aviso", "ID é obrigatório para edição.")
        return
    
    data = {
        "veiculo_id": int(veiculo_id) if veiculo_id else 0,
        "tipo_documento": tipo_documento,
        "numero_documento": numero_documento,
        "validade_inicio": validade_inicio,
        "validade_fim": validade_fim,
        "observacoes": observacoes
    }
    
    try:
        response = requests.put(f"{BASE_URL}/documentosveiculo/{id}/", json=data)
        if response.status_code == 200:
            messagebox.showinfo("Sucesso", "Documento atualizado com sucesso!")
        elif response.status_code == 201:
            messagebox.showinfo("Sucesso", "Documento atualizado com sucesso!")
        elif response.status_code == 404:
            messagebox.showerror("Erro", "Documento não encontrado.")
        else:
            messagebox.showerror("Erro", f"Erro ao atualizar documento: {response.text}")
    except Exception as e:
        messagebox.showerror("Erro", f"Falha na comunicação com a API: {str(e)}")

def excluir_documento(id):
    if not id:
        messagebox.showwarning("Aviso", "ID é obrigatório para exclusão.")
        return
    if not messagebox.askyesno("Confirmar", "Deseja realmente excluir este documento?"):
        return
    try:
        response = requests.delete(f"{BASE_URL}/documentosveiculo/{id}/")
        if response.status_code == 200:
            messagebox.showinfo("Sucesso", "Documento excluído com sucesso!")
        else:
            messagebox.showerror("Erro", f"Erro ao excluir documento: {response.text}")
    except Exception as e:
        messagebox.showerror("Erro", f"Falha na comunicação com a API: {str(e)}")

def buscar_documento(id, entry_veiculo_id, combo_tipo, entry_numero, entry_validade_inicio, entry_validade_fim, entry_observacoes):
    if not id:
        messagebox.showwarning("Aviso", "Informe o ID do documento")
        return
    try:
        response = requests.get(f"{BASE_URL}/documentosveiculo/{id}/")
        if response.status_code == 200:
            documento = response.json()
            entry_veiculo_id.delete(0, tk.END)
            entry_veiculo_id.insert(0, documento['veiculo_id'])
            combo_tipo.set(documento['tipo_documento'])
            entry_numero.delete(0, tk.END)
            entry_numero.insert(0, documento['numero_documento'])
            entry_validade_inicio.delete(0, tk.END)
            entry_validade_inicio.insert(0, documento['validade_inicio'])
            entry_validade_fim.delete(0, tk.END)
            entry_validade_fim.insert(0, documento['validade_fim'])
            entry_observacoes.delete(0, tk.END)
            entry_observacoes.insert(0, documento['observacoes'])
            messagebox.showinfo("Sucesso", "Documento encontrado")
        else:
            messagebox.showerror("Erro", f"Documento não encontrado: {response.text}")
    except Exception as e:
        messagebox.showerror("Erro", f"Falha na comunicação com a API: {str(e)}")

def buscar_todos_documentos():
    try:
        response = requests.get(f"{BASE_URL}/documentosveiculo/")
        if response.status_code == 200:
            documentos = response.json()
            mostrar_resultados_modal_documentos(documentos)
        else:
            messagebox.showerror("Erro", f"Erro ao buscar documentos: {response.text}")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro na comunicação com a API: {str(e)}")

def buscar_documentos_por_veiculo(veiculo_id):
    if not veiculo_id:
        messagebox.showwarning("Aviso", "Informe o ID do veículo")
        return
    try:
        response = requests.get(f"{BASE_URL}/documentosveiculo/veiculo/{veiculo_id}")
        if response.status_code == 200:
            documentos = response.json()
            mostrar_resultados_modal_documentos(documentos)
        else:
            messagebox.showerror("Erro", f"Erro ao buscar documentos: {response.text}")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro na comunicação com a API: {str(e)}")

def mostrar_resultados_modal_documentos(documentos):
    modal = tk.Toplevel()
    modal.title("Lista de Documentos")
    modal.geometry("1100x500")
    
    container = ttk.Frame(modal)
    container.pack(fill='both', expand=True)
    
    canvas = tk.Canvas(container, highlightthickness=0)
    scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    tree = ttk.Treeview(scrollable_frame, columns=("ID", "Veículo", "Tipo", "Número", "Validade Início", "Validade Fim", "Observações"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Veículo", text="ID Veículo")
    tree.heading("Tipo", text="Tipo Documento")
    tree.heading("Número", text="Número Documento")
    tree.heading("Validade Início", text="Validade Início")
    tree.heading("Validade Fim", text="Validade Fim")
    tree.heading("Observações", text="Observações")

    tree.column("ID", width=50, anchor='center')
    tree.column("Veículo", width=80, anchor='center')
    tree.column("Tipo", width=100, anchor='center')
    tree.column("Número", width=120, anchor='center')
    tree.column("Validade Início", width=100, anchor='center')
    tree.column("Validade Fim", width=100, anchor='center')
    tree.column("Observações", width=300)

    for documento in documentos:
        tree.insert("", "end", values=(
            documento['id'],
            documento['veiculo_id'],
            documento['tipo_documento'],
            documento['numero_documento'],
            documento['validade_inicio'],
            documento['validade_fim'],
            documento['observacoes']
        ))

    tree.pack(fill="both", expand=True, padx=10, pady=10)

    button_frame = ttk.Frame(modal)
    button_frame.pack(fill='x', pady=10)
    ttk.Button(button_frame, text="Fechar", command=modal.destroy).pack()

def limpar_formulario(entry_id, entry_veiculo_id, combo_tipo, entry_numero, entry_validade_inicio, 
                      entry_validade_fim, entry_observacoes,
                      entry_add_veiculo_id=None, combo_add_tipo=None, entry_add_numero=None, 
                      entry_add_validade_inicio=None, entry_add_validade_fim=None, entry_add_observacoes=None):
    entry_id.delete(0, tk.END)
    entry_veiculo_id.delete(0, tk.END)
    combo_tipo.set("CRLV")
    entry_numero.delete(0, tk.END)
    entry_validade_inicio.delete(0, tk.END)
    entry_validade_fim.delete(0, tk.END)
    entry_observacoes.delete(0, tk.END)
    
    if entry_add_veiculo_id:
        entry_add_veiculo_id.delete(0, tk.END)
    if combo_add_tipo:
        combo_add_tipo.set("CRLV")
    if entry_add_numero:
        entry_add_numero.delete(0, tk.END)
    if entry_add_validade_inicio:
        entry_add_validade_inicio.delete(0, tk.END)
    if entry_add_validade_fim:
        entry_add_validade_fim.delete(0, tk.END)
    if entry_add_observacoes:
        entry_add_observacoes.delete(0, tk.END)