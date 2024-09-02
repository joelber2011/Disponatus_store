import tkinter as tk
from tkinter import messagebox
import requests


class DisponatusApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Disponatus Store")
        self.root.geometry("800x600")

        self.token = None

        self.create_widgets()

    # ------------------------------------ WIDGETS / BUTTONS ----------------------------------------------------------

    def create_widgets(self):
        # Título na interface
        title_label = tk.Label(self.root, text="Bem-vindo à Disponatus Store", font=("Arial", 24))
        title_label.pack(pady=20)

        # Botões funcionais
        usuario_btn = tk.Button(self.root, text="Gerenciar Usuários", command=self.gerenciar_usuarios)
        usuario_btn.pack(pady=10)

        produto_btn = tk.Button(self.root, text="Gerenciar Produtos", command=self.gerenciar_produtos)
        produto_btn.pack(pady=10)

    # ------------------------------------ USUÁRIOS -------------------------------------------------------------------

    def gerenciar_usuarios(self):
        self.usuario_window = tk.Toplevel(self.root)
        self.usuario_window.title("Gerenciar Usuários")
        self.usuario_window.geometry("600x400")

        # Adicionando um título
        title = tk.Label(self.usuario_window, text="Lista de Usuários", font=("Arial", 18))
        title.pack(pady=10)

        # Simulação de uma lista de usuários
        usuarios_list = tk.Listbox(self.usuario_window)
        usuarios_list.pack(expand=True, fill="both", padx=20, pady=10)

        # Botão de adicionar usuário
        add_user_btn = tk.Button(self.usuario_window, text="Adicionar Usuário", command=self.adicionar_usuario)
        add_user_btn.pack(pady=10)

        # self.token = auth.login

    def adicionar_usuario(self):
        # Janela para adicionar um novo usuário
        add_window = tk.Toplevel(self.root)
        add_window.title("Adicionar Usuário")
        add_window.geometry("400x300")

        # Campos para nome, email e senha
        nome_label = tk.Label(add_window, text="Nome de Usuário")
        nome_label.pack(pady=5)
        nome_entry = tk.Entry(add_window)
        nome_entry.pack(pady=5)

        email_label = tk.Label(add_window, text="Email")
        email_label.pack(pady=5)
        email_entry = tk.Entry(add_window)
        email_entry.pack(pady=5)

        senha_label = tk.Label(add_window, text="Senha")
        senha_label.pack(pady=5)
        senha_entry = tk.Entry(add_window, show="*")
        senha_entry.pack(pady=5)

        # Botão para salvar o usuário
        salvar_btn = tk.Button(add_window, text="Salvar", command=lambda: self.salvar_usuario(nome_entry.get(), email_entry.get(), senha_entry.get()))
        salvar_btn.pack(pady=20)

    def salvar_usuario(self, nome, email, senha):
        url = "http://localhost:5000/register"  # URL da sua API Flask
        data = {
            "nome_usuario": nome,
            "email": email,
            "senha": senha
        }
        try:
            response = requests.post(url, json=data)

            if response.status_code == 201:
                messagebox.showinfo("Sucesso", f"Usuário {nome} adicionado com sucesso!")
            else:
                messagebox.showerror("Erro", f"Falha ao adicionar usuário: {response.json().get('message')}")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro de Conexão", f"Não foi possível conectar à API: {e}")

    # ------------------------------------ PRODUTOS -------------------------------------------------------------------

    def gerenciar_produtos(self):
        self.produto_window = tk.Toplevel(self.root)
        self.produto_window.title("Gerenciar Produtos")
        self.produto_window.geometry("600x400")

        title = tk.Label(self.produto_window, text="Lista de Produtos", font=("Arial", 18))
        title.pack(pady=10)

        produtos_list = tk.Listbox(self.produto_window)
        produtos_list.pack(expand=True, fill="both", padx=20, pady=10)

        add_produto_btn = tk.Button(self.produto_window, text="Adicionar Produto", command=self.adicionar_produto)
        add_produto_btn.pack(pady=10)

    def adicionar_produto(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Adicionar Produto")
        add_window.geometry("400x300")

        nome_label = tk.Label(add_window, text="Nome do Produto")
        nome_label.pack(pady=5)
        nome_entry = tk.Entry(add_window)
        nome_entry.pack(pady=5)

        preco_label = tk.Label(add_window, text="Preço")
        preco_label.pack(pady=5)
        preco_entry = tk.Entry(add_window)
        preco_entry.pack(pady=5)

        salvar_btn = tk.Button(add_window, text="Salvar",
                               command=lambda: self.salvar_produto(nome_entry.get(), preco_entry.get()))
        salvar_btn.pack(pady=20)

    def salvar_produto(self, nome, preco):
        url = "http://localhost:5000/produtos"  # URL da sua API Flask para adicionar produtos
        data = {
            "nome_produto": nome,
            "preco": preco
        }
        try:
            response = requests.post(url, json=data)

            if response.status_code == 201:
                messagebox.showinfo("Sucesso", f"Produto {nome} adicionado com sucesso!")
            else:
                messagebox.showerror("Erro", f"Falha ao adicionar produto: {response.json().get('message')}")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro de Conexão", f"Não foi possível conectar à API: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = DisponatusApp(root)
    root.mainloop()
