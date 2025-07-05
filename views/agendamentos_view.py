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
             text="Gerenciamento de Agendamentos", 
             font=('Segoe UI', 14, 'bold'), 
             foreground='#2b579a', 
             style='TLabel').pack(side='left')
    
    ttk.Label(main_frame, 
             text="Cadastre, edite e consulte os agendamentos da Old&Lux Rental Car", 
             font=('Segoe UI', 9), 
             foreground='#666666', 
             style='TLabel').pack(fill='x', pady=(0, 20), padx=20)

    add_frame = ttk.LabelFrame(main_frame, 
                              text="Novo Agendamento", 
                              padding=(15, 10),
                              style='TLabelframe')
    add_frame.pack(fill='x', pady=(0, 25), padx=20)
    
    ttk.Label(add_frame, text="Dados do Agendamento", style='TLabel').pack(anchor='w', pady=(0, 10))

    form_frame = ttk.Frame(add_frame, style='TFrame')
    form_frame.pack(fill='x')

    ttk.Label(form_frame, text="ID Cliente:", style='TLabel').grid(row=0, column=0, sticky='e', padx=5, pady=5)
    entry_cliente_id = ttk.Entry(form_frame, width=10, style='TEntry')
    entry_cliente_id.grid(row=0, column=1, sticky='w', padx=5, pady=5)

    ttk.Label(form_frame, text="ID Veículo:", style='TLabel').grid(row=0, column=2, sticky='e', padx=(15,5), pady=5)
    entry_veiculo_id = ttk.Entry(form_frame, width=10, style='TEntry')
    entry_veiculo_id.grid(row=0, column=3, sticky='w', padx=5, pady=5)

    ttk.Label(form_frame, text="Data Início (AAAA-MM-DD):", style='TLabel').grid(row=1, column=0, sticky='e', padx=5, pady=5)
    entry_data_inicio = ttk.Entry(form_frame, width=15, style='TEntry')
    entry_data_inicio.grid(row=1, column=1, sticky='w', padx=5, pady=5)

    ttk.Label(form_frame, text="Data Fim (AAAA-MM-DD):", style='TLabel').grid(row=1, column=2, sticky='e', padx=(15,5), pady=5)
    entry_data_fim = ttk.Entry(form_frame, width=15, style='TEntry')
    entry_data_fim.grid(row=1, column=3, sticky='w', padx=5, pady=5)

    ttk.Label(form_frame, text="Status:", style='TLabel').grid(row=2, column=0, sticky='e', padx=(15,5), pady=5)
    status_options = ["agendado", "em_andamento", "concluido", "cancelado"]
    combo_status = ttk.Combobox(form_frame, values=status_options, width=15, state="readonly")
    combo_status.grid(row=2, column=1, sticky='w', padx=5, pady=5)
    combo_status.set("agendado")

    ttk.Label(form_frame, text="KM Retirada:", style='TLabel').grid(row=3, column=0, sticky='e', padx=5, pady=5)
    entry_km_retirada = ttk.Entry(form_frame, width=10, style='TEntry')
    entry_km_retirada.grid(row=3, column=1, sticky='w', padx=5, pady=5)

    ttk.Label(form_frame, text="KM Devolução:", style='TLabel').grid(row=3, column=2, sticky='e', padx=(15,5), pady=5)
    entry_km_devolucao = ttk.Entry(form_frame, width=10, style='TEntry')
    entry_km_devolucao.grid(row=3, column=3, sticky='w', padx=5, pady=5)

    btn_frame = ttk.Frame(add_frame, style='TFrame')
    btn_frame.pack(fill='x', pady=(10, 0))
    
    btn_salvar = ttk.Button(btn_frame, 
                          text="Salvar", 
                          command=lambda: adicionar_agendamento(
                              entry_cliente_id.get(),
                              entry_veiculo_id.get(),
                              entry_data_inicio.get(),
                              entry_data_fim.get(),
                              entry_km_retirada.get(),
                              entry_km_devolucao.get(),
                              combo_status.get()
                          ), 
                          style='Accent.TButton')
    btn_salvar.pack(side='left', padx=5)

    edit_frame = ttk.LabelFrame(main_frame, 
                               text="Editar Agendamento", 
                               padding=(15, 10),
                               style='TLabelframe')
    edit_frame.pack(fill='x', pady=(0, 15), padx=20)
    
    ttk.Label(edit_frame, text="Dados do Agendamento", style='TLabel').pack(anchor='w', pady=(0, 10))

    edit_form_frame = ttk.Frame(edit_frame, style='TFrame')
    edit_form_frame.pack(fill='x')

    ttk.Label(edit_form_frame, text="ID Agendamento:", style='TLabel').grid(row=0, column=0, sticky='e', padx=5, pady=5)
    entry_id = ttk.Entry(edit_form_frame, width=10, style='TEntry')
    entry_id.grid(row=0, column=1, sticky='w', padx=5, pady=5)

    ttk.Label(edit_form_frame, text="ID Cliente:", style='TLabel').grid(row=1, column=0, sticky='e', padx=5, pady=5)
    entry_edit_cliente_id = ttk.Entry(edit_form_frame, width=10, style='TEntry')
    entry_edit_cliente_id.grid(row=1, column=1, sticky='w', padx=5, pady=5)

    ttk.Label(edit_form_frame, text="ID Veículo:", style='TLabel').grid(row=1, column=2, sticky='e', padx=(15,5), pady=5)
    entry_edit_veiculo_id = ttk.Entry(edit_form_frame, width=10, style='TEntry')
    entry_edit_veiculo_id.grid(row=1, column=3, sticky='w', padx=5, pady=5)

    ttk.Label(edit_form_frame, text="Data Início:", style='TLabel').grid(row=2, column=0, sticky='e', padx=5, pady=5)
    entry_edit_data_inicio = ttk.Entry(edit_form_frame, width=15, style='TEntry')
    entry_edit_data_inicio.grid(row=2, column=1, sticky='w', padx=5, pady=5)

    ttk.Label(edit_form_frame, text="Data Fim:", style='TLabel').grid(row=2, column=2, sticky='e', padx=(15,5), pady=5)
    entry_edit_data_fim = ttk.Entry(edit_form_frame, width=15, style='TEntry')
    entry_edit_data_fim.grid(row=2, column=3, sticky='w', padx=5, pady=5)

    ttk.Label(edit_form_frame, text="KM Retirada:", style='TLabel').grid(row=3, column=0, sticky='e', padx=5, pady=5)
    entry_edit_km_retirada = ttk.Entry(edit_form_frame, width=10, style='TEntry')
    entry_edit_km_retirada.grid(row=3, column=1, sticky='w', padx=5, pady=5)

    ttk.Label(edit_form_frame, text="KM Devolução:", style='TLabel').grid(row=3, column=2, sticky='e', padx=(15,5), pady=5)
    entry_edit_km_devolucao = ttk.Entry(edit_form_frame, width=10, style='TEntry')
    entry_edit_km_devolucao.grid(row=3, column=3, sticky='w', padx=5, pady=5)

    ttk.Label(edit_form_frame, text="Status:", style='TLabel').grid(row=4, column=0, sticky='e', padx=5, pady=5)
    edit_status_options = ["agendado", "em_andamento", "concluido", "cancelado"]
    combo_edit_status = ttk.Combobox(edit_form_frame, values=edit_status_options, width=15, state="readonly")
    combo_edit_status.grid(row=4, column=1, sticky='w', padx=5, pady=5)

    button_frame = ttk.Frame(edit_frame, style='TFrame')
    button_frame.pack(fill='x', pady=(15, 5))

    btn_editar = ttk.Button(button_frame, 
                           text="Editar", 
                           command=lambda: editar_agendamento(
                               entry_id.get(),
                               entry_edit_cliente_id.get(),
                               entry_edit_veiculo_id.get(),
                               entry_edit_data_inicio.get(),
                               entry_edit_data_fim.get(),
                               entry_edit_km_retirada.get(),
                               entry_edit_km_devolucao.get(),
                               combo_edit_status.get()
                           ))
    btn_editar.pack(side='left', padx=5)

    btn_excluir = ttk.Button(button_frame, 
                            text="Excluir", 
                            command=lambda: excluir_agendamento(entry_id.get()), 
                            style='Danger.TButton')
    btn_excluir.pack(side='left', padx=5)

    btn_buscar = ttk.Button(button_frame, 
                           text="Buscar", 
                           command=lambda: buscar_agendamento(
                               entry_id.get(),
                               entry_edit_cliente_id,
                               entry_edit_veiculo_id,
                               entry_edit_data_inicio,
                               entry_edit_data_fim,
                               entry_edit_km_retirada,
                               entry_edit_km_devolucao,
                               combo_edit_status
                           ))
    btn_buscar.pack(side='left', padx=5)

    btn_buscar_todos = ttk.Button(button_frame, 
                                 text="Buscar Todos", 
                                 command=buscar_todos_agendamentos)
    btn_buscar_todos.pack(side='left', padx=5)

    btn_buscar_veiculo = ttk.Button(button_frame, 
                                   text="Por Veículo", 
                                   command=lambda: buscar_agendamentos_por_veiculo(entry_edit_veiculo_id.get()))
    btn_buscar_veiculo.pack(side='left', padx=5)

    btn_buscar_cliente = ttk.Button(button_frame, 
                                   text="Por Cliente", 
                                   command=lambda: buscar_agendamentos_por_cliente(entry_edit_cliente_id.get()))
    btn_buscar_cliente.pack(side='left', padx=5)

    btn_limpar = ttk.Button(button_frame, 
                           text="Limpar", 
                           command=lambda: limpar_formulario(
                               entry_id,
                               entry_edit_cliente_id,
                               entry_edit_veiculo_id,
                               entry_edit_data_inicio,
                               entry_edit_data_fim,
                               entry_edit_km_retirada,
                               entry_edit_km_devolucao,
                               combo_edit_status,
                               entry_cliente_id,
                               entry_veiculo_id,
                               entry_data_inicio,
                               entry_data_fim,
                               entry_km_retirada,
                               combo_status
                           ))
    btn_limpar.pack(side='left', padx=5)

    concluir_frame = ttk.LabelFrame(main_frame, 
                                   text="Concluir Agendamento", 
                                   padding=(15, 10),
                                   style='TLabelframe')
    concluir_frame.pack(fill='x', pady=(0, 15), padx=20)
    
    ttk.Label(concluir_frame, text="Dados para Conclusão", style='TLabel').pack(anchor='w', pady=(0, 10))

    concluir_form_frame = ttk.Frame(concluir_frame, style='TFrame')
    concluir_form_frame.pack(fill='x')

    ttk.Label(concluir_form_frame, text="ID Agendamento:", style='TLabel').grid(row=0, column=0, sticky='e', padx=5, pady=5)
    entry_concluir_id = ttk.Entry(concluir_form_frame, width=10, style='TEntry')
    entry_concluir_id.grid(row=0, column=1, sticky='w', padx=5, pady=5)

    ttk.Label(concluir_form_frame, text="KM Devolução:", style='TLabel').grid(row=1, column=0, sticky='e', padx=5, pady=5)
    entry_concluir_km_devolucao = ttk.Entry(concluir_form_frame, width=10, style='TEntry')
    entry_concluir_km_devolucao.grid(row=1, column=1, sticky='w', padx=5, pady=5)

    concluir_btn_frame = ttk.Frame(concluir_frame, style='TFrame')
    concluir_btn_frame.pack(fill='x', pady=(10, 0))
    
    btn_concluir = ttk.Button(concluir_btn_frame, 
                             text="Concluir Agendamento", 
                             command=lambda: concluir_agendamento(
                                 entry_concluir_id.get(),
                                 entry_concluir_km_devolucao.get()
                             ),
                             style='Success.TButton')
    btn_concluir.pack(side='left', padx=5)

    style.configure('Accent.TButton', foreground='white', background='#2b579a')
    style.configure('Danger.TButton', foreground='white', background='#d83b01')
    style.configure('Success.TButton', foreground='white', background='#107c10')

    return main_frame

def adicionar_agendamento(cliente_id, veiculo_id, data_inicio, data_fim, km_retirada,
                          km_devolucao, status):
    data = {
        "cliente_id": int(cliente_id) if cliente_id else 0,
        "veiculo_id": int(veiculo_id) if veiculo_id else 0,
        "data_inicio": data_inicio,
        "data_fim": data_fim,
        "quilometragem_retirada": int(km_retirada) if km_retirada else 0,
        "quilometragem_devolucao": int(km_devolucao) if km_devolucao else 0,
        "status": status.lower()
    }
    
    if not cliente_id or not veiculo_id or not data_inicio or not data_fim:
        messagebox.showwarning("Aviso", "Cliente, Veículo, Data Início e Data Fim são obrigatórios!")
        return
    
    try:
        response = requests.post(f"{BASE_URL}/agendamentos/", json=data)
        if response.status_code == 201:
            messagebox.showinfo("Sucesso", "Agendamento cadastrado com sucesso!")
        else:
            messagebox.showerror("Erro", f"Erro ao cadastrar agendamento: {response.text}")
    except Exception as e:
        messagebox.showerror("Erro", f"Falha na comunicação com a API: {str(e)}")

def editar_agendamento(id, cliente_id, veiculo_id, data_inicio, data_fim, km_retirada, km_devolucao, status):
    if not id:
        messagebox.showwarning("Aviso", "ID é obrigatório para edição.")
        return
    
    data = {
        "cliente_id": int(cliente_id) if cliente_id else 0,
        "veiculo_id": int(veiculo_id) if veiculo_id else 0,
        "data_inicio": data_inicio,
        "data_fim": data_fim,
        "quilometragem_retirada": int(km_retirada) if km_retirada else 0,
        "quilometragem_devolucao": int(km_devolucao) if km_devolucao else 0,
        "status": status.lower()
    }
    
    try:
        response = requests.put(f"{BASE_URL}/agendamentos/{id}/", json=data)
        if response.status_code == 200:
            messagebox.showinfo("Sucesso", "Agendamento atualizado com sucesso!")
        elif response.status_code == 201:
            messagebox.showinfo("Sucesso", "Agendamento atualizado com sucesso!")
        elif response.status_code == 404:
            messagebox.showerror("Erro", "Agendamento não encontrado.")
        else:
            messagebox.showerror("Erro", f"Erro ao atualizar agendamento: {response.text}")
    except Exception as e:
        messagebox.showerror("Erro", f"Falha na comunicação com a API: {str(e)}")

def excluir_agendamento(id):
    if not id:
        messagebox.showwarning("Aviso", "ID é obrigatório para exclusão.")
        return
    if not messagebox.askyesno("Confirmar", "Deseja realmente excluir este agendamento?"):
        return
    try:
        response = requests.delete(f"{BASE_URL}/agendamentos/{id}/")
        if response.status_code == 200:
            messagebox.showinfo("Sucesso", "Agendamento excluído com sucesso!")
        else:
            messagebox.showerror("Erro", f"Erro ao excluir agendamento: {response.text}")
    except Exception as e:
        messagebox.showerror("Erro", f"Falha na comunicação com a API: {str(e)}")

def buscar_agendamento(id, entry_cliente_id, entry_veiculo_id, entry_data_inicio, entry_data_fim, 
                      entry_km_retirada, entry_km_devolucao, combo_status):
    if not id:
        messagebox.showwarning("Aviso", "Informe o ID do agendamento")
        return
    try:
        response = requests.get(f"{BASE_URL}/agendamentos/{id}/")
        if response.status_code == 200:
            agendamento = response.json()
            entry_cliente_id.delete(0, tk.END)
            entry_cliente_id.insert(0, agendamento['cliente_id'])
            entry_veiculo_id.delete(0, tk.END)
            entry_veiculo_id.insert(0, agendamento['veiculo_id'])
            entry_data_inicio.delete(0, tk.END)
            entry_data_inicio.insert(0, agendamento['data_inicio'])
            entry_data_fim.delete(0, tk.END)
            entry_data_fim.insert(0, agendamento['data_fim'])
            entry_km_retirada.delete(0, tk.END)
            entry_km_retirada.insert(0, agendamento['quilometragem_retirada'])
            entry_km_devolucao.delete(0, tk.END)
            entry_km_devolucao.insert(0, agendamento['quilometragem_devolucao'])
            combo_status.set(agendamento['status'])
            messagebox.showinfo("Sucesso", "Agendamento encontrado")
        else:
            messagebox.showerror("Erro", f"Agendamento não encontrado: {response.text}")
    except Exception as e:
        messagebox.showerror("Erro", f"Falha na comunicação com a API: {str(e)}")

def buscar_todos_agendamentos():
    try:
        response = requests.get(f"{BASE_URL}/agendamentos/")
        if response.status_code == 200:
            agendamentos = response.json()
            mostrar_resultados_modal_agendamentos(agendamentos)
        else:
            messagebox.showerror("Erro", f"Erro ao buscar agendamentos: {response.text}")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro na comunicação com a API: {str(e)}")

def buscar_agendamentos_por_veiculo(veiculo_id):
    if not veiculo_id:
        messagebox.showwarning("Aviso", "Informe o ID do veículo")
        return
    try:
        response = requests.get(f"{BASE_URL}/agendamentos/veiculo/{veiculo_id}")
        if response.status_code == 200:
            agendamentos = response.json()
            mostrar_resultados_modal_agendamentos(agendamentos)
        else:
            messagebox.showerror("Erro", f"Erro ao buscar agendamentos: {response.text}")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro na comunicação com a API: {str(e)}")

def buscar_agendamentos_por_cliente(cliente_id):
    if not cliente_id:
        messagebox.showwarning("Aviso", "Informe o ID do cliente")
        return
    try:
        response = requests.get(f"{BASE_URL}/agendamentos/cliente/{cliente_id}")
        if response.status_code == 200:
            agendamentos = response.json()
            mostrar_resultados_modal_agendamentos(agendamentos)
        else:
            messagebox.showerror("Erro", f"Erro ao buscar agendamentos: {response.text}")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro na comunicação com a API: {str(e)}")

def concluir_agendamento(agendamento_id, km_devolucao):
    if not agendamento_id:
        messagebox.showwarning("Aviso", "Informe o ID do agendamento")
        return
    if not km_devolucao:
        messagebox.showwarning("Aviso", "Informe a quilometragem de devolução")
        return
    
    try:
        km_devolucao_int = int(km_devolucao)
        params = {'quilometragem_devolucao': km_devolucao_int}
        response = requests.put(
            f"{BASE_URL}/agendamentos/{agendamento_id}/concluir",
            params=params
        )
        
        if response.status_code == 200:
            resposta = response.json()
            valor_total = resposta.get('valor_total', 'Valor não disponível')
            mensagem = (
                f"Agendamento concluído com sucesso!\n"
                f"Valor total a pagar: R$ {valor_total}"
            )
            messagebox.showinfo("Sucesso", mensagem)
        else:
            messagebox.showerror("Erro", f"Erro ao concluir agendamento: {response.text}")
    except ValueError:
        messagebox.showerror("Erro", "Quilometragem deve ser um número inteiro")
    except Exception as e:
        messagebox.showerror("Erro", f"Falha na comunicação com a API: {str(e)}")

def mostrar_resultados_modal_agendamentos(agendamentos):
    modal = tk.Toplevel()
    modal.title("Lista de Agendamentos")
    modal.geometry("1000x500")
    
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

    tree = ttk.Treeview(scrollable_frame, columns=("ID", "Cliente", "Veículo", "Início", "Fim", "KM Retirada", "KM Devolução", "Status"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Cliente", text="ID Cliente")
    tree.heading("Veículo", text="ID Veículo")
    tree.heading("Início", text="Data Início")
    tree.heading("Fim", text="Data Fim")
    tree.heading("KM Retirada", text="KM Retirada")
    tree.heading("KM Devolução", text="KM Devolução")
    tree.heading("Status", text="Status")

    tree.column("ID", width=50, anchor='center')
    tree.column("Cliente", width=80, anchor='center')
    tree.column("Veículo", width=80, anchor='center')
    tree.column("Início", width=100, anchor='center')
    tree.column("Fim", width=100, anchor='center')
    tree.column("KM Retirada", width=90, anchor='center')
    tree.column("KM Devolução", width=90, anchor='center')
    tree.column("Status", width=100, anchor='center')

    for agendamento in agendamentos:
        tree.insert("", "end", values=(
            agendamento['id'],
            agendamento['cliente_id'],
            agendamento['veiculo_id'],
            agendamento['data_inicio'],
            agendamento['data_fim'],
            agendamento['quilometragem_retirada'],
            agendamento['quilometragem_devolucao'],
            agendamento['status']
        ))

    tree.pack(fill="both", expand=True, padx=10, pady=10)

    button_frame = ttk.Frame(modal)
    button_frame.pack(fill='x', pady=10)
    ttk.Button(button_frame, text="Fechar", command=modal.destroy).pack()

def limpar_formulario(entry_id, entry_cliente_id, entry_veiculo_id, entry_data_inicio, entry_data_fim, 
                      entry_km_retirada, entry_km_devolucao, combo_status,
                      entry_add_cliente_id=None, entry_add_veiculo_id=None, entry_add_data_inicio=None, 
                      entry_add_data_fim=None, entry_add_km_retirada=None, combo_add_status=None,
                      entry_concluir_id=None, entry_concluir_km=None):
    entry_id.delete(0, tk.END)
    entry_cliente_id.delete(0, tk.END)
    entry_veiculo_id.delete(0, tk.END)
    entry_data_inicio.delete(0, tk.END)
    entry_data_fim.delete(0, tk.END)
    entry_km_retirada.delete(0, tk.END)
    entry_km_devolucao.delete(0, tk.END)
    combo_status.set("agendado")
    
    if entry_add_cliente_id:
        entry_add_cliente_id.delete(0, tk.END)
    if entry_add_veiculo_id:
        entry_add_veiculo_id.delete(0, tk.END)
    if entry_add_data_inicio:
        entry_add_data_inicio.delete(0, tk.END)
    if entry_add_data_fim:
        entry_add_data_fim.delete(0, tk.END)
    if entry_add_km_retirada:
        entry_add_km_retirada.delete(0, tk.END)
    if combo_add_status:
        combo_add_status.set("agendado")
    if entry_concluir_id:
        entry_concluir_id.delete(0, tk.END)
    if entry_concluir_km:
        entry_concluir_km.delete(0, tk.END)