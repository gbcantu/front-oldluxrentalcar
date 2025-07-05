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
             text="Gerenciamento de Manutenções", 
             font=('Segoe UI', 14, 'bold'), 
             foreground='#2b579a', 
             style='TLabel').pack(side='left')
    
    ttk.Label(main_frame, 
             text="Cadastre, edite e consulte as manutenções da Old&Lux Rental Car", 
             font=('Segoe UI', 9), 
             foreground='#666666', 
             style='TLabel').pack(fill='x', pady=(0, 20), padx=20)

    add_frame = ttk.LabelFrame(main_frame, 
                              text="Nova Manutenção", 
                              padding=(15, 10),
                              style='TLabelframe')
    add_frame.pack(fill='x', pady=(0, 25), padx=20)
    
    ttk.Label(add_frame, text="Dados da Manutenção", style='TLabel').pack(anchor='w', pady=(0, 10))

    form_frame = ttk.Frame(add_frame, style='TFrame')
    form_frame.pack(fill='x')

    ttk.Label(form_frame, text="ID Veículo:", style='TLabel').grid(row=0, column=0, sticky='e', padx=5, pady=5)
    entry_veiculo_id = ttk.Entry(form_frame, width=10, style='TEntry')
    entry_veiculo_id.grid(row=0, column=1, sticky='w', padx=5, pady=5)

    ttk.Label(form_frame, text="Tipo:", style='TLabel').grid(row=0, column=2, sticky='e', padx=(15,5), pady=5)
    tipo_options = ["Preventiva", "Corretiva", "Pintura", "Elétrica", "Mecânica", "Outros"]
    combo_tipo = ttk.Combobox(form_frame, values=tipo_options, width=15, state="readonly")
    combo_tipo.grid(row=0, column=3, sticky='w', padx=5, pady=5)
    combo_tipo.set("Preventiva")

    ttk.Label(form_frame, text="Data (AAAA-MM-DD):", style='TLabel').grid(row=1, column=0, sticky='e', padx=5, pady=5)
    entry_data = ttk.Entry(form_frame, width=15, style='TEntry')
    entry_data.grid(row=1, column=1, sticky='w', padx=5, pady=5)

    ttk.Label(form_frame, text="Quilometragem:", style='TLabel').grid(row=1, column=2, sticky='e', padx=(15,5), pady=5)
    entry_km = ttk.Entry(form_frame, width=10, style='TEntry')
    entry_km.grid(row=1, column=3, sticky='w', padx=5, pady=5)

    ttk.Label(form_frame, text="Custo (R$):", style='TLabel').grid(row=2, column=0, sticky='e', padx=5, pady=5)
    entry_custo = ttk.Entry(form_frame, width=10, style='TEntry')
    entry_custo.grid(row=2, column=1, sticky='w', padx=5, pady=5)

    ttk.Label(form_frame, text="Descrição:", style='TLabel').grid(row=3, column=0, sticky='e', padx=5, pady=5)
    entry_descricao = ttk.Entry(form_frame, width=50, style='TEntry')
    entry_descricao.grid(row=3, column=1, sticky='w', padx=5, pady=5, columnspan=3)

    btn_frame = ttk.Frame(add_frame, style='TFrame')
    btn_frame.pack(fill='x', pady=(10, 0))
    
    btn_salvar = ttk.Button(btn_frame, 
                          text="Salvar", 
                          command=lambda: adicionar_manutencao(
                              entry_veiculo_id.get(),
                              combo_tipo.get(),
                              entry_data.get(),
                              entry_descricao.get(),
                              entry_custo.get(),
                              entry_km.get()
                          ), 
                          style='Accent.TButton')
    btn_salvar.pack(side='left', padx=5)

    edit_frame = ttk.LabelFrame(main_frame, 
                               text="Editar Manutenção", 
                               padding=(15, 10),
                               style='TLabelframe')
    edit_frame.pack(fill='x', pady=(0, 15), padx=20)
    
    ttk.Label(edit_frame, text="Dados da Manutenção", style='TLabel').pack(anchor='w', pady=(0, 10))

    edit_form_frame = ttk.Frame(edit_frame, style='TFrame')
    edit_form_frame.pack(fill='x')

    ttk.Label(edit_form_frame, text="ID Manutenção:", style='TLabel').grid(row=0, column=0, sticky='e', padx=5, pady=5)
    entry_id = ttk.Entry(edit_form_frame, width=10, style='TEntry')
    entry_id.grid(row=0, column=1, sticky='w', padx=5, pady=5)

    ttk.Label(edit_form_frame, text="ID Veículo:", style='TLabel').grid(row=1, column=0, sticky='e', padx=5, pady=5)
    entry_edit_veiculo_id = ttk.Entry(edit_form_frame, width=10, style='TEntry')
    entry_edit_veiculo_id.grid(row=1, column=1, sticky='w', padx=5, pady=5)

    ttk.Label(edit_form_frame, text="Tipo:", style='TLabel').grid(row=1, column=2, sticky='e', padx=(15,5), pady=5)
    edit_tipo_options = ["Preventiva", "Corretiva", "Pintura", "Elétrica", "Mecânica", "Outros"]
    combo_edit_tipo = ttk.Combobox(edit_form_frame, values=edit_tipo_options, width=15, state="readonly")
    combo_edit_tipo.grid(row=1, column=3, sticky='w', padx=5, pady=5)

    ttk.Label(edit_form_frame, text="Data:", style='TLabel').grid(row=2, column=0, sticky='e', padx=5, pady=5)
    entry_edit_data = ttk.Entry(edit_form_frame, width=15, style='TEntry')
    entry_edit_data.grid(row=2, column=1, sticky='w', padx=5, pady=5)

    ttk.Label(edit_form_frame, text="Quilometragem:", style='TLabel').grid(row=2, column=2, sticky='e', padx=(15,5), pady=5)
    entry_edit_km = ttk.Entry(edit_form_frame, width=10, style='TEntry')
    entry_edit_km.grid(row=2, column=3, sticky='w', padx=5, pady=5)

    ttk.Label(edit_form_frame, text="Custo (R$):", style='TLabel').grid(row=3, column=0, sticky='e', padx=5, pady=5)
    entry_edit_custo = ttk.Entry(edit_form_frame, width=10, style='TEntry')
    entry_edit_custo.grid(row=3, column=1, sticky='w', padx=5, pady=5)

    ttk.Label(edit_form_frame, text="Descrição:", style='TLabel').grid(row=4, column=0, sticky='e', padx=5, pady=5)
    entry_edit_descricao = ttk.Entry(edit_form_frame, width=50, style='TEntry')
    entry_edit_descricao.grid(row=4, column=1, sticky='w', padx=5, pady=5, columnspan=3)

    button_frame = ttk.Frame(edit_frame, style='TFrame')
    button_frame.pack(fill='x', pady=(15, 5))

    btn_editar = ttk.Button(button_frame, 
                           text="Editar", 
                           command=lambda: editar_manutencao(
                               entry_id.get(),
                               entry_edit_veiculo_id.get(),
                               combo_edit_tipo.get(),
                               entry_edit_data.get(),
                               entry_edit_descricao.get(),
                               entry_edit_custo.get(),
                               entry_edit_km.get()
                           ))
    btn_editar.pack(side='left', padx=5)

    btn_excluir = ttk.Button(button_frame, 
                            text="Excluir", 
                            command=lambda: excluir_manutencao(entry_id.get()), 
                            style='Danger.TButton')
    btn_excluir.pack(side='left', padx=5)

    btn_buscar = ttk.Button(button_frame, 
                           text="Buscar", 
                           command=lambda: buscar_manutencao(
                               entry_id.get(),
                               entry_edit_veiculo_id,
                               combo_edit_tipo,
                               entry_edit_data,
                               entry_edit_descricao,
                               entry_edit_custo,
                               entry_edit_km
                           ))
    btn_buscar.pack(side='left', padx=5)

    btn_buscar_todos = ttk.Button(button_frame, 
                                 text="Buscar Todos", 
                                 command=buscar_todos_manutencoes)
    btn_buscar_todos.pack(side='left', padx=5)

    btn_buscar_veiculo = ttk.Button(button_frame, 
                                   text="Por Veículo", 
                                   command=lambda: buscar_manutencoes_por_veiculo(entry_edit_veiculo_id.get()))
    btn_buscar_veiculo.pack(side='left', padx=5)

    btn_limpar = ttk.Button(button_frame, 
                           text="Limpar", 
                           command=lambda: limpar_formulario(
                               entry_id,
                               entry_edit_veiculo_id,
                               combo_edit_tipo,
                               entry_edit_data,
                               entry_edit_descricao,
                               entry_edit_custo,
                               entry_edit_km,
                               entry_veiculo_id,
                               combo_tipo,
                               entry_data,
                               entry_descricao,
                               entry_custo,
                               entry_km
                           ))
    btn_limpar.pack(side='left', padx=5)

    style.configure('Accent.TButton', foreground='white', background='#2b579a')
    style.configure('Danger.TButton', foreground='white', background='#d83b01')

    return main_frame

def adicionar_manutencao(veiculo_id, tipo, data, descricao, custo, quilometragem):
    data = {
        "veiculo_id": int(veiculo_id) if veiculo_id else 0,
        "tipo": tipo,
        "data": data,
        "descricao": descricao,
        "custo": float(custo) if custo else 0.0,
        "quilometragem": int(quilometragem) if quilometragem else 0
    }
    
    if not veiculo_id or not tipo or not data:
        messagebox.showwarning("Aviso", "Veículo, Tipo e Data são obrigatórios!")
        return
    
    try:
        response = requests.post(f"{BASE_URL}/manutencao/", json=data)
        if response.status_code == 201:
            messagebox.showinfo("Sucesso", "Manutenção cadastrada com sucesso!")
        else:
            messagebox.showerror("Erro", f"Erro ao cadastrar manutenção: {response.text}")
    except Exception as e:
        messagebox.showerror("Erro", f"Falha na comunicação com a API: {str(e)}")

def editar_manutencao(id, veiculo_id, tipo, data, descricao, custo, quilometragem):
    if not id:
        messagebox.showwarning("Aviso", "ID é obrigatório para edição.")
        return
    
    data = {
        "veiculo_id": int(veiculo_id) if veiculo_id else 0,
        "tipo": tipo,
        "data": data,
        "descricao": descricao,
        "custo": float(custo) if custo else 0.0,
        "quilometragem": int(quilometragem) if quilometragem else 0
    }
    
    try:
        response = requests.put(f"{BASE_URL}/manutencao/{id}/", json=data)
        if response.status_code == 200:
            messagebox.showinfo("Sucesso", "Manutenção atualizada com sucesso!")
        elif response.status_code == 201:
            messagebox.showinfo("Sucesso", "Manutenção atualizada com sucesso!")
        elif response.status_code == 404:
            messagebox.showerror("Erro", "Manutenção não encontrada.")
        else:
            messagebox.showerror("Erro", f"Erro ao atualizar manutenção: {response.text}")
    except Exception as e:
        messagebox.showerror("Erro", f"Falha na comunicação com a API: {str(e)}")

def excluir_manutencao(id):
    if not id:
        messagebox.showwarning("Aviso", "ID é obrigatório para exclusão.")
        return
    if not messagebox.askyesno("Confirmar", "Deseja realmente excluir esta manutenção?"):
        return
    try:
        response = requests.delete(f"{BASE_URL}/manutencao/{id}/")
        if response.status_code == 200:
            messagebox.showinfo("Sucesso", "Manutenção excluída com sucesso!")
        else:
            messagebox.showerror("Erro", f"Erro ao excluir manutenção: {response.text}")
    except Exception as e:
        messagebox.showerror("Erro", f"Falha na comunicação com a API: {str(e)}")

def buscar_manutencao(id, entry_veiculo_id, combo_tipo, entry_data, entry_descricao, entry_custo, entry_km):
    if not id:
        messagebox.showwarning("Aviso", "Informe o ID da manutenção")
        return
    try:
        response = requests.get(f"{BASE_URL}/manutencao/{id}/")
        if response.status_code == 200:
            manutencao = response.json()
            entry_veiculo_id.delete(0, tk.END)
            entry_veiculo_id.insert(0, manutencao['veiculo_id'])
            combo_tipo.set(manutencao['tipo'])
            entry_data.delete(0, tk.END)
            entry_data.insert(0, manutencao['data'])
            entry_descricao.delete(0, tk.END)
            entry_descricao.insert(0, manutencao['descricao'])
            entry_custo.delete(0, tk.END)
            entry_custo.insert(0, manutencao['custo'])
            entry_km.delete(0, tk.END)
            entry_km.insert(0, manutencao['quilometragem'])
            messagebox.showinfo("Sucesso", "Manutenção encontrada")
        else:
            messagebox.showerror("Erro", f"Manutenção não encontrada: {response.text}")
    except Exception as e:
        messagebox.showerror("Erro", f"Falha na comunicação com a API: {str(e)}")

def buscar_todos_manutencoes():
    try:
        response = requests.get(f"{BASE_URL}/manutencao/")
        if response.status_code == 200:
            manutencoes = response.json()
            mostrar_resultados_modal_manutencoes(manutencoes)
        else:
            messagebox.showerror("Erro", f"Erro ao buscar manutenções: {response.text}")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro na comunicação com a API: {str(e)}")

def buscar_manutencoes_por_veiculo(veiculo_id):
    if not veiculo_id:
        messagebox.showwarning("Aviso", "Informe o ID do veículo")
        return
    try:
        response = requests.get(f"{BASE_URL}/manutencao/veiculo/{veiculo_id}/")
        if response.status_code == 200:
            manutencoes = response.json()
            mostrar_resultados_modal_manutencoes(manutencoes)
        else:
            messagebox.showerror("Erro", f"Erro ao buscar manutenções: {response.text}")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro na comunicação com a API: {str(e)}")

def mostrar_resultados_modal_manutencoes(manutencoes):
    modal = tk.Toplevel()
    modal.title("Lista de Manutenções")
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

    tree = ttk.Treeview(scrollable_frame, columns=("ID", "Veículo", "Tipo", "Data", "Descrição", "Custo", "Quilometragem"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Veículo", text="ID Veículo")
    tree.heading("Tipo", text="Tipo")
    tree.heading("Data", text="Data")
    tree.heading("Descrição", text="Descrição")
    tree.heading("Custo", text="Custo (R$)")
    tree.heading("Quilometragem", text="Quilometragem")

    tree.column("ID", width=50, anchor='center')
    tree.column("Veículo", width=80, anchor='center')
    tree.column("Tipo", width=100, anchor='center')
    tree.column("Data", width=100, anchor='center')
    tree.column("Descrição", width=300)
    tree.column("Custo", width=80, anchor='center')
    tree.column("Quilometragem", width=100, anchor='center')

    for manutencao in manutencoes:
        tree.insert("", "end", values=(
            manutencao['id'],
            manutencao['veiculo_id'],
            manutencao['tipo'],
            manutencao['data'],
            manutencao['descricao'],
            manutencao['custo'],
            manutencao['quilometragem']
        ))

    tree.pack(fill="both", expand=True, padx=10, pady=10)

    button_frame = ttk.Frame(modal)
    button_frame.pack(fill='x', pady=10)
    ttk.Button(button_frame, text="Fechar", command=modal.destroy).pack()

def limpar_formulario(entry_id, entry_veiculo_id, combo_tipo, entry_data, entry_descricao, entry_custo, entry_km,
                      entry_add_veiculo_id=None, combo_add_tipo=None, entry_add_data=None, 
                      entry_add_descricao=None, entry_add_custo=None, entry_add_km=None):
    entry_id.delete(0, tk.END)
    entry_veiculo_id.delete(0, tk.END)
    combo_tipo.set("Preventiva")
    entry_data.delete(0, tk.END)
    entry_descricao.delete(0, tk.END)
    entry_custo.delete(0, tk.END)
    entry_km.delete(0, tk.END)
    
    if entry_add_veiculo_id:
        entry_add_veiculo_id.delete(0, tk.END)
    if combo_add_tipo:
        combo_add_tipo.set("Preventiva")
    if entry_add_data:
        entry_add_data.delete(0, tk.END)
    if entry_add_descricao:
        entry_add_descricao.delete(0, tk.END)
    if entry_add_custo:
        entry_add_custo.delete(0, tk.END)
    if entry_add_km:
        entry_add_km.delete(0, tk.END)