
## Sistema de Gestão Interna – Old&Lux Rental Car

##### Este projeto é um sistema de gestão interna desenvolvido para a fictícia locadora de veículos **Old&Lux Rental Car**, especializada em automóveis antigos e luxuosos. Criado como parte da disciplina **PAV – Programação em Ambiente Visual**, o sistema permite a administração eficiente de veículos, reservas e clientes.

## 🚀 Tecnologias Utilizadas
Controle de aluguéis e reservas.

- Python 3.x  
- FastAPI  
- Uvicorn  
- PostgreSql (mas atualmente adaptado para Sqlite3)
- Outras dependências especificadas em `requirements.txt`

## ⚙️ Configuração do Ambiente
### 1. Criar o Ambiente Virtual
No terminal, execute:

`python -m venv venv`

### 2. Ativar o Ambiente Virtual (Windows)

`venv\Scripts\activate`

#### ⚠️ Se houver erro de permissão, use:

`Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process`
#### Em seguida, ative novamente:

`venv\Scripts\activate`

### 3. Instalar as Dependências
#### Com o ambiente virtual ativado, execute:

`pip install -r requirements.txt`

### 4. Como Executar o Projeto
#### Inicie a interface grafica:

`python main.py`
