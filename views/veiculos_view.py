import tkinter as tk
from tkinter import ttk, messagebox
import requests

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
    main_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=main_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    title_frame = ttk.Frame(main_frame, style='TFrame')
    title_frame.pack(fill='x', pady=(0, 20), padx=20)
    ttk.Label(title_frame, text="Gerenciamento de Veículos", font=('Segoe UI', 14, 'bold'), foreground='#2b579a', style='TLabel').pack(side='left')
    ttk.Label(main_frame, text="Cadastre, edite e consulte os veículos da Old&Lux Rental Car", font=('Segoe UI', 9), foreground='#666666', style='TLabel').pack(fill='x', pady=(0, 20), padx=20)

    add_frame = ttk.LabelFrame(main_frame, text="Adicionar Veículo", padding=(15, 10), style='TLabelframe')
    add_frame.pack(fill='x', pady=(0, 25), padx=20)
    ttk.Label(add_frame, text="Dados do Veículo", style='TLabel').pack(anchor='w', pady=(0, 10))
    form_frame = ttk.Frame(add_frame, style='TFrame')
    form_frame.pack(fill='x')

    ttk.Label(form_frame, text="Modelo:", style='TLabel').grid(row=0, column=0, sticky='e', padx=5, pady=5)
    entry_modelo = ttk.Entry(form_frame, width=30, style='TEntry')
    entry_modelo.grid(row=0, column=1, sticky='ew', padx=5, pady=5, columnspan=3)

    ttk.Label(form_frame, text="Marca:", style='TLabel').grid(row=0, column=4, sticky='e', padx=(15,5), pady=5)
    entry_marca = ttk.Entry(form_frame, width=20, style='TEntry')
    entry_marca.grid(row=0, column=5, sticky='ew', padx=5, pady=5)

    ttk.Label(form_frame, text="Ano Fabricação:", style='TLabel').grid(row=1, column=0, sticky='e', padx=5, pady=5)
    entry_ano = ttk.Entry(form_frame, width=10, style='TEntry')
    entry_ano.grid(row=1, column=1, sticky='w', padx=5, pady=5)

    ttk.Label(form_frame, text="Placa:", style='TLabel').grid(row=1, column=2, sticky='e', padx=(15,5), pady=5)
    entry_placa = ttk.Entry(form_frame, width=12, style='TEntry')
    entry_placa.grid(row=1, column=3, sticky='w', padx=5, pady=5)

    ttk.Label(form_frame, text="Valor Diária:", style='TLabel').grid(row=2, column=0, sticky='e', padx=5, pady=5)
    entry_valor = ttk.Entry(form_frame, width=12, style='TEntry')
    entry_valor.grid(row=2, column=1, sticky='w', padx=5, pady=5)

    ttk.Label(form_frame, text="Quilometragem:", style='TLabel').grid(row=2, column=2, sticky='e', padx=(15,5), pady=5)
    entry_km = ttk.Entry(form_frame, width=12, style='TEntry')
    entry_km.grid(row=2, column=3, sticky='w', padx=5, pady=5)

    disponivel_var = tk.BooleanVar(value=True)
    ttk.Checkbutton(form_frame, text="Disponível", variable=disponivel_var, style='TLabel').grid(row=3, column=1, sticky='w', padx=5, pady=(10,5))

    btn_frame = ttk.Frame(add_frame, style='TFrame')
    btn_frame.pack(fill='x', pady=(10, 0))
    btn_salvar = ttk.Button(btn_frame, text="Salvar", command=lambda: adicionar_veiculo(entry_modelo.get(), entry_marca.get(), entry_ano.get(), entry_placa.get(), entry_valor.get(), entry_km.get(), disponivel_var.get()), style='Accent.TButton')
    btn_salvar.pack(side='left', padx=5)

    edit_frame = ttk.LabelFrame(main_frame, text="Editar Veículos", padding=(15, 10), style='TLabelframe')
    edit_frame.pack(fill='x', pady=(0, 15), padx=20)
    ttk.Label(edit_frame, text="Dados do Veículo", style='TLabel').pack(anchor='w', pady=(0, 10))
    edit_form_frame = ttk.Frame(edit_frame, style='TFrame')
    edit_form_frame.pack(fill='x')

    ttk.Label(edit_form_frame, text="ID:", style='TLabel').grid(row=0, column=0, sticky='e', padx=5, pady=5)
    entry_id = ttk.Entry(edit_form_frame, width=8, style='TEntry')
    entry_id.grid(row=0, column=1, sticky='w', padx=5, pady=5)

    ttk.Label(edit_form_frame, text="Modelo:", style='TLabel').grid(row=1, column=0, sticky='e', padx=5, pady=5)
    entry_edit_modelo = ttk.Entry(edit_form_frame, width=30, style='TEntry')
    entry_edit_modelo.grid(row=1, column=1, sticky='ew', padx=5, pady=5, columnspan=3)

    ttk.Label(edit_form_frame, text="Marca:", style='TLabel').grid(row=1, column=4, sticky='e', padx=(15,5), pady=5)
    entry_edit_marca = ttk.Entry(edit_form_frame, width=20, style='TEntry')
    entry_edit_marca.grid(row=1, column=5, sticky='ew', padx=5, pady=5)

    ttk.Label(edit_form_frame, text="Ano Fabricação:", style='TLabel').grid(row=2, column=0, sticky='e', padx=5, pady=5)
    entry_edit_ano = ttk.Entry(edit_form_frame, width=10, style='TEntry')
    entry_edit_ano.grid(row=2, column=1, sticky='w', padx=5, pady=5)

    ttk.Label(edit_form_frame, text="Placa:", style='TLabel').grid(row=2, column=2, sticky='e', padx=(15,5), pady=5)
    entry_edit_placa = ttk.Entry(edit_form_frame, width=12, style='TEntry')
    entry_edit_placa.grid(row=2, column=3, sticky='w', padx=5, pady=5)

    ttk.Label(edit_form_frame, text="Valor Diária:", style='TLabel').grid(row=3, column=0, sticky='e', padx=5, pady=5)
    entry_edit_valor = ttk.Entry(edit_form_frame, width=12, style='TEntry')
    entry_edit_valor.grid(row=3, column=1, sticky='w', padx=5, pady=5)

    ttk.Label(edit_form_frame, text="Quilometragem:", style='TLabel').grid(row=3, column=2, sticky='e', padx=(15,5), pady=5)
    entry_edit_km = ttk.Entry(edit_form_frame, width=12, style='TEntry')
    entry_edit_km.grid(row=3, column=3, sticky='w', padx=5, pady=5)

    edit_disponivel_var = tk.BooleanVar(value=True)
    ttk.Checkbutton(edit_form_frame, text="Disponível", variable=edit_disponivel_var, style='TLabel').grid(row=4, column=1, sticky='w', padx=5, pady=(10,5))

    button_frame = ttk.Frame(edit_frame, style='TFrame')
    button_frame.pack(fill='x', pady=(15, 5))

    btn_editar = ttk.Button(button_frame, text="Editar", command=lambda: editar_veiculo(entry_id.get(), entry_edit_modelo.get(), entry_edit_marca.get(), entry_edit_ano.get(), entry_edit_placa.get(), entry_edit_valor.get(), entry_edit_km.get(), edit_disponivel_var.get()))
    btn_editar.pack(side='left', padx=5)

    btn_excluir = ttk.Button(button_frame, text="Excluir", command=lambda: excluir_veiculo(entry_id.get()), style='Danger.TButton')
    btn_excluir.pack(side='left', padx=5)

    btn_buscar = ttk.Button(button_frame, text="Buscar", command=lambda: buscar_veiculo(entry_id.get(), entry_edit_modelo, entry_edit_marca, entry_edit_ano, entry_edit_placa, entry_edit_valor, entry_edit_km, edit_disponivel_var))
    btn_buscar.pack(side='left', padx=5)

    btn_buscar_todos = ttk.Button(button_frame, text="Buscar Todos", command=buscar_todos_veiculos)
    btn_buscar_todos.pack(side='left', padx=5)

    btn_limpar = ttk.Button(button_frame, text="Limpar", command=lambda: limpar_formulario(entry_id, entry_edit_modelo, entry_edit_marca, entry_edit_ano, entry_edit_placa, entry_edit_valor, entry_edit_km, entry_modelo, entry_marca, entry_ano, entry_placa, entry_valor, entry_km))
    btn_limpar.pack(side='left', padx=5)

    style.configure('Accent.TButton', foreground='white', background='#2b579a')
    style.configure('Danger.TButton', foreground='white', background='#d83b01')

    return main_frame

def adicionar_veiculo(modelo, marca, ano_fabricacao, placa, valor_diaria, quilometragem, disponivel):
    data = {
        "modelo": modelo,
        "marca": marca,
        "ano_fabricacao": int(ano_fabricacao) if ano_fabricacao else 0,
        "placa": placa,
        "valor_diaria": valor_diaria,
        "quilometragem_atual": int(quilometragem) if quilometragem else 0,
        "disponivel": disponivel
    }
    try:
        response = requests.post(f"{BASE_URL}/veiculos/", json=data)
        if response.status_code == 201:
            messagebox.showinfo("Sucesso", "Veículo cadastrado com sucesso!")
        else:
            messagebox.showerror("Erro", f"Erro ao cadastrar veículo: {response.text}")
    except Exception as e:
        messagebox.showerror("Erro", f"Falha na comunicação com a API: {str(e)}")

def editar_veiculo(id, modelo, marca, ano_fabricacao, placa, valor_diaria, quilometragem, disponivel):
    if not id:
        messagebox.showwarning("Aviso", "ID é obrigatório para edição.")
        return
    data = {
        "modelo": modelo,
        "marca": marca,
        "ano_fabricacao": int(ano_fabricacao) if ano_fabricacao else 0,
        "placa": placa,
        "valor_diaria": valor_diaria,
        "quilometragem_atual": int(quilometragem) if quilometragem else 0,
        "disponivel": disponivel
    }
    try:
        response = requests.put(f"{BASE_URL}/veiculos/{id}/", json=data)
        if response.status_code == 200:
            messagebox.showinfo("Sucesso", "Veículo atualizado com sucesso!")
        elif response.status_code == 404:
            messagebox.showerror("Erro", "Veículo não encontrado.")
        elif response.status_code == 201:
            messagebox.showinfo("Sucesso", "Veículo atualizado com sucesso!")
        else:
            messagebox.showwarning("Aviso", f"Alterações aplicadas, mas a API retornou: {response.status_code}\n{response.text}")
    except Exception as e:
        messagebox.showerror("Erro", f"Falha na comunicação com a API: {str(e)}")

def excluir_veiculo(id):
    if not id:
        messagebox.showwarning("Aviso", "ID é obrigatório para exclusão.")
        return
    if not messagebox.askyesno("Confirmar", "Deseja realmente excluir este veículo?"):
        return
    try:
        response = requests.delete(f"{BASE_URL}/veiculos/{id}/")
        if response.status_code == 200:
            messagebox.showinfo("Sucesso", "Veículo excluído com sucesso!")
        else:
            messagebox.showerror("Erro", f"Erro ao excluir veículo: {response.text}")
    except Exception as e:
        messagebox.showerror("Erro", f"Falha na comunicação com a API: {str(e)}")

def buscar_veiculo(id, entry_modelo, entry_marca, entry_ano, entry_placa, entry_valor, entry_km, entry_disponivel):
    if not id:
        messagebox.showwarning("Aviso", "Informe o ID do veículo")
        return
    try:
        response = requests.get(f"{BASE_URL}/veiculos/{id}/")
        if response.status_code == 200:
            veiculo = response.json()
            entry_modelo.delete(0, tk.END)
            entry_modelo.insert(0, veiculo['modelo'])
            entry_marca.delete(0, tk.END)
            entry_marca.insert(0, veiculo['marca'])
            entry_ano.delete(0, tk.END)
            entry_ano.insert(0, veiculo['ano_fabricacao'])
            entry_placa.delete(0, tk.END)
            entry_placa.insert(0, veiculo['placa'])
            entry_valor.delete(0, tk.END)
            entry_valor.insert(0, veiculo['valor_diaria'])
            entry_km.delete(0, tk.END)
            entry_km.insert(0, veiculo['quilometragem_atual'])
            entry_disponivel.set(veiculo['disponivel'])
            messagebox.showinfo("Sucesso", "Veículo encontrado")
        else:
            messagebox.showerror("Erro", f"Veículo não encontrado: {response.text}")
    except Exception as e:
        messagebox.showerror("Erro", f"Falha na comunicação com a API: {str(e)}")

def buscar_todos_veiculos():
    try:
        response = requests.get(f"{BASE_URL}/veiculos/")
        if response.status_code == 200:
            veiculos = response.json()
            mostrar_resultados_modal_veiculos(veiculos)
        else:
            messagebox.showerror("Erro", f"Erro ao buscar veículos: {response.text}")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro na comunicação com a API: {str(e)}")

def mostrar_resultados_modal_veiculos(veiculos):
    modal = tk.Toplevel()
    modal.title("Lista de Veículos")
    modal.geometry("800x400")
    container = ttk.Frame(modal)
    container.pack(fill='both', expand=True)
    canvas = tk.Canvas(container, highlightthickness=0)
    scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    tree = ttk.Treeview(scrollable_frame, columns=("ID", "Modelo", "Marca", "Ano", "Placa", "Valor Diária", "KM", "Disponível"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Modelo", text="Modelo")
    tree.heading("Marca", text="Marca")
    tree.heading("Ano", text="Ano")
    tree.heading("Placa", text="Placa")
    tree.heading("Valor Diária", text="Valor Diária")
    tree.heading("KM", text="Quilometragem")
    tree.heading("Disponível", text="Disponível")
    tree.column("ID", width=50, anchor='center')
    tree.column("Modelo", width=120)
    tree.column("Marca", width=80)
    tree.column("Ano", width=60, anchor='center')
    tree.column("Placa", width=80, anchor='center')
    tree.column("Valor Diária", width=90, anchor='center')
    tree.column("KM", width=80, anchor='center')
    tree.column("Disponível", width=80, anchor='center')

    for veiculo in veiculos:
        tree.insert("", "end", values=(veiculo['id'], veiculo['modelo'], veiculo['marca'], veiculo['ano_fabricacao'], veiculo['placa'], veiculo['valor_diaria'], veiculo['quilometragem_atual'], "Sim" if veiculo['disponivel'] else "Não"))

    tree.pack(fill="both", expand=True, padx=10, pady=10)
    button_frame = ttk.Frame(modal)
    button_frame.pack(fill='x', pady=10)
    ttk.Button(button_frame, text="Fechar", command=modal.destroy).pack()

def limpar_formulario(entry_id, entry_modelo, entry_marca, entry_ano, entry_placa, entry_valor, entry_km, entry_add_modelo=None, entry_add_marca=None, entry_add_ano=None, entry_add_placa=None, entry_add_valor=None, entry_add_km=None):
    entry_id.delete(0, tk.END)
    entry_modelo.delete(0, tk.END)
    entry_marca.delete(0, tk.END)
    entry_ano.delete(0, tk.END)
    entry_placa.delete(0, tk.END)
    entry_valor.delete(0, tk.END)
    entry_km.delete(0, tk.END)
    if entry_add_modelo:
        entry_add_modelo.delete(0, tk.END)
    if entry_add_marca:
        entry_add_marca.delete(0, tk.END)
    if entry_add_ano:
        entry_add_ano.delete(0, tk.END)
    if entry_add_placa:
        entry_add_placa.delete(0, tk.END)
    if entry_add_valor:
        entry_add_valor.delete(0, tk.END)
    if entry_add_km:
        entry_add_km.delete(0, tk.END)
