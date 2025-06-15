# tela_produtos.py
import customtkinter as ctk
from tkinter import messagebox
import gerenciador_dados as gd
import time

class TelaGerenciamentoProdutos(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master # Referência à janela principal App
        self.title("Gerenciamento de Produtos")
        self.geometry("600x450")
        self.resizable(False, False)

        self.produtos = gd.carregar_dados(gd.ARQUIVO_PRODUTOS)
        self.produto_selecionado_id = ctk.StringVar()

        # Frame principal
        self.frame_principal = ctk.CTkFrame(self)
        self.frame_principal.pack(expand=True, fill="both", padx=10, pady=10)

        # Frame da tabela
        self.frame_tabela = ctk.CTkScrollableFrame(self.frame_principal, label_text="Produtos Cadastrados")
        self.frame_tabela.pack(expand=True, fill="both", padx=5, pady=5)
        self.frame_tabela.grid_columnconfigure(1, weight=1) # Coluna do nome do produto expande

        # Frame dos botões
        self.frame_botoes = ctk.CTkFrame(self.frame_principal)
        self.frame_botoes.pack(fill="x", padx=5, pady=5)
        
        self.btn_adicionar = ctk.CTkButton(self.frame_botoes, text="Adicionar Produto", command=self.adicionar_produto)
        self.btn_adicionar.pack(side="left", padx=10, pady=10)

        self.btn_excluir = ctk.CTkButton(self.frame_botoes, text="Excluir Selecionado", command=self.excluir_produto, fg_color="red", hover_color="#9B0000")
        self.btn_excluir.pack(side="right", padx=10, pady=10)

        self.protocol("WM_DELETE_WINDOW", self.fechar_janela) # Garante que o dropdown será atualizado ao fechar no 'X'

        self.atualizar_tabela()

    def atualizar_tabela(self):
        # Limpa a tabela antiga
        for widget in self.frame_tabela.winfo_children():
            widget.destroy()

        # Adiciona cabeçalhos
        ctk.CTkLabel(self.frame_tabela, text="ID", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=10, pady=5)
        ctk.CTkLabel(self.frame_tabela, text="Nome do Produto", font=ctk.CTkFont(weight="bold")).grid(row=0, column=1, padx=10, pady=5, sticky="w")
        ctk.CTkLabel(self.frame_tabela, text="Preço", font=ctk.CTkFont(weight="bold")).grid(row=0, column=2, padx=10, pady=5)
        ctk.CTkLabel(self.frame_tabela, text="Sel.", font=ctk.CTkFont(weight="bold")).grid(row=0, column=3, padx=5, pady=5)

        # Preenche a tabela com os produtos
        self.produtos = gd.carregar_dados(gd.ARQUIVO_PRODUTOS)
        for i, produto in enumerate(self.produtos, start=1):
            ctk.CTkLabel(self.frame_tabela, text=produto['id']).grid(row=i, column=0, padx=10)
            ctk.CTkLabel(self.frame_tabela, text=produto['nome']).grid(row=i, column=1, padx=10, sticky="w")
            ctk.CTkLabel(self.frame_tabela, text=f"R$ {produto['preco']:.2f}").grid(row=i, column=2, padx=10)
            
            radio_btn = ctk.CTkRadioButton(self.frame_tabela, text="", variable=self.produto_selecionado_id, value=str(produto['id']))
            radio_btn.grid(row=i, column=3, padx=5)

    def adicionar_produto(self):
        dialog = ctk.CTkInputDialog(text="Digite o nome do novo produto:", title="Adicionar Produto")
        nome_produto = dialog.get_input()

        if nome_produto:
            dialog_preco = ctk.CTkInputDialog(text=f"Digite o preço para '{nome_produto}':", title="Adicionar Preço")
            preco_str = dialog_preco.get_input()
            try:
                preco = float(preco_str.replace(",", "."))
                
                novo_id = int(time.time()) # Usando timestamp como ID simples
                novo_produto = {"id": novo_id, "nome": nome_produto, "preco": preco}
                
                self.produtos.append(novo_produto)
                gd.salvar_dados(gd.ARQUIVO_PRODUTOS, self.produtos)
                self.atualizar_tabela()

            except (ValueError, TypeError):
                messagebox.showerror("Erro", "Preço inválido. Por favor, insira um número.")

    def excluir_produto(self):
        id_selecionado = self.produto_selecionado_id.get()
        if not id_selecionado:
            messagebox.showwarning("Aviso", "Por favor, selecione um produto para excluir.")
            return

        confirmar = messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja excluir o produto com ID {id_selecionado}?")
        
        if confirmar:
            self.produtos = [p for p in self.produtos if str(p['id']) != id_selecionado]
            gd.salvar_dados(gd.ARQUIVO_PRODUTOS, self.produtos)
            self.produto_selecionado_id.set("") # Limpa a seleção
            self.atualizar_tabela()
    
    def fechar_janela(self):
        self.master.atualizar_dropdown_produtos() # Chama o método da janela principal
        self.destroy()