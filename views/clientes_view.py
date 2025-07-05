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
    
    ttk.Label(title_frame, text="Gerenciamento de Clientes", font=('Segoe UI', 14, 'bold'), foreground='#2b579a', style='TLabel').pack(side='left')
    ttk.Label(main_frame, text="Cadastre, edite e consulte os clientes da Old&Lux Rental Car", font=('Segoe UI', 9), foreground='#666666', style='TLabel').pack(fill='x', pady=(0, 20), padx=20)

    add_frame = ttk.LabelFrame(main_frame, text="Adicionar Clientes", padding=(15, 10), style='TLabelframe')
    add_frame.pack(fill='x', pady=(0, 25), padx=20)
    
    ttk.Label(add_frame, text="Dados do Cliente", style='TLabel').pack(anchor='w', pady=(0, 10))

    form_frame = ttk.Frame(add_frame, style='TFrame')
    form_frame.pack(fill='x')

    ttk.Label(form_frame, text="Nome completo:", style='TLabel').grid(row=0, column=0, sticky='e', padx=5, pady=5)
    entry_nome = ttk.Entry(form_frame, width=40, style='TEntry')
    entry_nome.grid(row=0, column=1, sticky='ew', padx=5, pady=5, columnspan=3)

    ttk.Label(form_frame, text="CPF:", style='TLabel').grid(row=1, column=0, sticky='e', padx=5, pady=5)
    entry_cpf = ttk.Entry(form_frame, width=20, style='TEntry')
    entry_cpf.grid(row=1, column=1, sticky='w', padx=5, pady=5)

    ttk.Label(form_frame, text="E-mail:", style='TLabel').grid(row=2, column=0, sticky='e', padx=5, pady=5)
    entry_email = ttk.Entry(form_frame, width=40, style='TEntry')
    entry_email.grid(row=2, column=1, sticky='ew', padx=5, pady=5, columnspan=3)

    ttk.Label(form_frame, text="Telefone:", style='TLabel').grid(row=3, column=0, sticky='e', padx=5, pady=5)
    entry_telefone = ttk.Entry(form_frame, width=20, style='TEntry')
    entry_telefone.grid(row=3, column=1, sticky='w', padx=5, pady=5)

    btn_frame = ttk.Frame(add_frame, style='TFrame')
    btn_frame.pack(fill='x', pady=(10, 0))
    
    btn_salvar = ttk.Button(btn_frame, text="Salvar", command=lambda: adicionar_cliente(entry_nome.get(), entry_cpf.get(), entry_email.get(), entry_telefone.get()), style='Accent.TButton')
    btn_salvar.pack(side='left', padx=5)

    edit_frame = ttk.LabelFrame(main_frame, text="Editar Clientes", padding=(15, 10), style='TLabelframe')
    edit_frame.pack(fill='x', pady=(0, 15), padx=20)
    
    ttk.Label(edit_frame, text="Dados do Cliente", style='TLabel').pack(anchor='w', pady=(0, 10))

    edit_form_frame = ttk.Frame(edit_frame, style='TFrame')
    edit_form_frame.pack(fill='x')

    ttk.Label(edit_form_frame, text="ID:", style='TLabel').grid(row=0, column=0, sticky='e', padx=5, pady=5)
    entry_id = ttk.Entry(edit_form_frame, width=8, style='TEntry')
    entry_id.grid(row=0, column=1, sticky='w', padx=5, pady=5)

    ttk.Label(edit_form_frame, text="Nome completo:", style='TLabel').grid(row=1, column=0, sticky='e', padx=5, pady=5)
    entry_edit_nome = ttk.Entry(edit_form_frame, width=40, style='TEntry')
    entry_edit_nome.grid(row=1, column=1, sticky='ew', padx=5, pady=5, columnspan=3)

    ttk.Label(edit_form_frame, text="CPF:", style='TLabel').grid(row=2, column=0, sticky='e', padx=5, pady=5)
    entry_edit_cpf = ttk.Entry(edit_form_frame, width=20, style='TEntry')
    entry_edit_cpf.grid(row=2, column=1, sticky='w', padx=5, pady=5)

    ttk.Label(edit_form_frame, text="E-mail:", style='TLabel').grid(row=3, column=0, sticky='e', padx=5, pady=5)
    entry_edit_email = ttk.Entry(edit_form_frame, width=40, style='TEntry')
    entry_edit_email.grid(row=3, column=1, sticky='ew', padx=5, pady=5, columnspan=3)

    ttk.Label(edit_form_frame, text="Telefone:", style='TLabel').grid(row=4, column=0, sticky='e', padx=5, pady=5)
    entry_edit_telefone = ttk.Entry(edit_form_frame, width=20, style='TEntry')
    entry_edit_telefone.grid(row=4, column=1, sticky='w', padx=5, pady=5)

    button_frame = ttk.Frame(edit_frame, style='TFrame')
    button_frame.pack(fill='x', pady=(15, 5))

    btn_editar = ttk.Button(button_frame, text="Editar", command=lambda: editar_cliente(entry_id.get(), entry_edit_nome.get(), entry_edit_cpf.get(), entry_edit_email.get(), entry_edit_telefone.get()))
    btn_editar.pack(side='left', padx=5)

    btn_excluir = ttk.Button(button_frame, text="Excluir", command=lambda: excluir_cliente(entry_id.get()), style='Danger.TButton')
    btn_excluir.pack(side='left', padx=5)

    btn_buscar = ttk.Button(button_frame, text="Buscar", command=lambda: buscar_cliente(entry_id.get(), entry_edit_nome, entry_edit_cpf, entry_edit_email, entry_edit_telefone))
    btn_buscar.pack(side='left', padx=5)

    btn_buscar_todos = ttk.Button(button_frame, text="Buscar Todos", command=buscar_todos)
    btn_buscar_todos.pack(side='left', padx=5)

    btn_limpar = ttk.Button(button_frame, text="Limpar", command=lambda: limpar_formulario(entry_id, entry_edit_nome, entry_edit_cpf, entry_edit_email, entry_edit_telefone, entry_nome, entry_cpf, entry_email, entry_telefone))
    btn_limpar.pack(side='left', padx=5)

    style.configure('Accent.TButton', foreground='white', background='#2b579a')
    style.configure('Danger.TButton', foreground='white', background='#d83b01')

    return main_frame

def adicionar_cliente(nome, cpf, email, telefone):
    data = {"nome": nome, "cpf": cpf, "email": email, "telefone": telefone}
    try:
        response = requests.post(f"{BASE_URL}/clientes/", json=data)
        if response.status_code == 201:
            messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")
        else:
            messagebox.showerror("Erro", f"Erro ao cadastrar cliente: {response.text}")
    except Exception as e:
        messagebox.showerror("Erro", f"Falha na comunicação com a API: {str(e)}")

def editar_cliente(id, nome, cpf, email, telefone):
    if not id:
        messagebox.showwarning("Aviso", "ID é obrigatório para edição.")
        return
    data = {"nome": nome, "cpf": cpf, "email": email, "telefone": telefone}
    try:
        response = requests.put(f"{BASE_URL}/clientes/{id}/", json=data)
        if response.status_code == 200:
            messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso!")
        elif response.status_code == 404:
            messagebox.showerror("Erro", "Cliente não encontrado.")
        elif response.status_code == 201:
            messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso!")
        else:
            messagebox.showwarning("Aviso", f"Alterações aplicadas, mas a API retornou: {response.status_code}\n{response.text}")
    except Exception as e:
        messagebox.showerror("Erro", f"Falha na comunicação com a API: {str(e)}")

def excluir_cliente(id):
    if not id:
        messagebox.showwarning("Aviso", "ID é obrigatório para exclusão.")
        return
    if not messagebox.askyesno("Confirmar", "Deseja realmente excluir este cliente?"):
        return
    try:
        response = requests.delete(f"{BASE_URL}/clientes/{id}/")
        if response.status_code == 200:
            messagebox.showinfo("Sucesso", "Cliente excluído com sucesso!")
        else:
            messagebox.showerror("Erro", f"Erro ao excluir cliente: {response.text}")
    except Exception as e:
        messagebox.showerror("Erro", f"Falha na comunicação com a API: {str(e)}")

def buscar_cliente(id, entry_nome, entry_cpf, entry_email, entry_telefone):
    if not id:
        messagebox.showwarning("Aviso", "Informe o ID do cliente")
        return
    try:
        response = requests.get(f"{BASE_URL}/clientes/{id}/")
        if response.status_code == 200:
            cliente = response.json()
            entry_nome.delete(0, tk.END)
            entry_nome.insert(0, cliente['nome'])
            entry_cpf.delete(0, tk.END)
            entry_cpf.insert(0, cliente['cpf'])
            entry_email.delete(0, tk.END)
            entry_email.insert(0, cliente['email'])
            entry_telefone.delete(0, tk.END)
            entry_telefone.insert(0, cliente['telefone'])
            messagebox.showinfo("Sucesso", "Cliente encontrado")
        else:
            messagebox.showerror("Erro", f"Cliente não encontrado: {response.text}")
    except Exception as e:
        messagebox.showerror("Erro", f"Falha na comunicação com a API: {str(e)}")

def buscar_todos():
    try:
        response = requests.get(f"{BASE_URL}/clientes/")
        if response.status_code == 200:
            clientes = response.json()
            mostrar_resultados_modal(clientes)
        else:
            messagebox.showerror("Erro", f"Erro ao buscar clientes: {response.text}")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro na comunicação com a API: {str(e)}")

def mostrar_resultados_modal(clientes):
    modal = tk.Toplevel()
    modal.title("Lista de Clientes")
    modal.geometry("700x400")

    tree = ttk.Treeview(modal, columns=("ID", "Nome", "CPF", "Email", "Telefone"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Nome", text="Nome")
    tree.heading("CPF", text="CPF")
    tree.heading("Email", text="E-mail")
    tree.heading("Telefone", text="Telefone")

    tree.column("ID", width=50, anchor='center')
    tree.column("Nome", width=150)
    tree.column("CPF", width=100)
    tree.column("Email", width=150)
    tree.column("Telefone", width=100)

    for cliente in clientes:
        tree.insert("", "end", values=(cliente['id'], cliente['nome'], cliente['cpf'], cliente['email'], cliente['telefone']))

    tree.pack(fill="both", expand=True, padx=10, pady=10)

    ttk.Button(modal, text="Fechar", command=modal.destroy).pack(pady=10)

def limpar_formulario(entry_id, entry_nome, entry_cpf, entry_email, entry_telefone, entry_add_nome=None, entry_add_cpf=None, entry_add_email=None, entry_add_telefone=None):
    entry_id.delete(0, tk.END)
    entry_nome.delete(0, tk.END)
    entry_cpf.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_telefone.delete(0, tk.END)
    if entry_add_nome:
        entry_add_nome.delete(0, tk.END)
    if entry_add_cpf:
        entry_add_cpf.delete(0, tk.END)
    if entry_add_email:
        entry_add_email.delete(0, tk.END)
    if entry_add_telefone:
        entry_add_telefone.delete(0, tk.END)
