import customtkinter as ctk
from tkinter import messagebox
import gerenciador_dados as gd
import time

class DialogoProduto(ctk.CTkToplevel):
    """
    Diálogo personalizado para adicionar ou editar produtos.
    """
    def __init__(self, master, produto_existente=None):
        super().__init__(master)
        
        self.produto = None
        self.produto_existente = produto_existente
        
        self.title("Adicionar Produto" if not produto_existente else "Editar Produto")
        self.geometry("350x250")
        self.resizable(False, False)
        self.transient(master) # Mantém o diálogo na frente da janela principal
        self.grab_set()

        # Obter categorias existentes para o ComboBox
        produtos = gd.carregar_dados(gd.ARQUIVO_PRODUTOS)
        categorias = sorted(list(set(p['categoria'] for p in produtos if 'categoria' in p)))

        ctk.CTkLabel(self, text="Nome:").pack(padx=20, pady=(10, 0))
        self.entry_nome = ctk.CTkEntry(self, width=300)
        self.entry_nome.pack(padx=20)
        
        ctk.CTkLabel(self, text="Preço:").pack(padx=20, pady=(10, 0))
        self.entry_preco = ctk.CTkEntry(self, width=300)
        self.entry_preco.pack(padx=20)

        ctk.CTkLabel(self, text="Categoria:").pack(padx=20, pady=(10, 0))
        self.combo_categoria = ctk.CTkComboBox(self, width=300, values=categorias)
        self.combo_categoria.pack(padx=20)

        # Preencher campos se estiver editando
        if produto_existente:
            self.entry_nome.insert(0, produto_existente.get('nome', ''))
            self.entry_preco.insert(0, str(produto_existente.get('preco', '')))
            self.combo_categoria.set(produto_existente.get('categoria', ''))
        else:
             self.combo_categoria.set(categorias[0] if categorias else "")

        btn_salvar = ctk.CTkButton(self, text="Salvar", command=self.salvar)
        btn_salvar.pack(pady=20)

    def salvar(self):
        nome = self.entry_nome.get().strip()
        preco_str = self.entry_preco.get().strip()
        categoria = self.combo_categoria.get().strip()

        if not nome or not preco_str or not categoria:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios.", parent=self)
            return
        
        try:
            preco = float(preco_str.replace(",", "."))
        except ValueError:
            messagebox.showerror("Erro", "Preço inválido.", parent=self)
            return

        self.produto = {
            "id": self.produto_existente['id'] if self.produto_existente else int(time.time()),
            "nome": nome,
            "preco": preco,
            "categoria": categoria
        }
        self.destroy()

    def get_produto(self):
        self.wait_window()
        return self.produto


class TelaGerenciamentoProdutos(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.title("Gerenciamento de Produtos")
        self.geometry("700x500") # Aumentado para nova coluna
        self.resizable(False, False)

        # ... (código do __init__ continua igual até a criação dos botões) ...
        self.produtos = gd.carregar_dados(gd.ARQUIVO_PRODUTOS)
        self.produto_selecionado_id = ctk.StringVar()

        self.frame_principal = ctk.CTkFrame(self)
        self.frame_principal.pack(expand=True, fill="both", padx=10, pady=10)

        self.frame_tabela = ctk.CTkScrollableFrame(self.frame_principal, label_text="Produtos Cadastrados")
        self.frame_tabela.pack(expand=True, fill="both", padx=5, pady=5)
        self.frame_tabela.grid_columnconfigure(1, weight=1)

        self.frame_botoes = ctk.CTkFrame(self.frame_principal)
        self.frame_botoes.pack(fill="x", padx=5, pady=5)
        
        self.btn_adicionar = ctk.CTkButton(self.frame_botoes, text="Adicionar Produto", command=self.adicionar_produto)
        self.btn_adicionar.pack(side="left", padx=10, pady=10)
        
        # Opcional: Adicionar botão de Editar
        # self.btn_editar = ctk.CTkButton(self.frame_botoes, text="Editar Selecionado", command=self.editar_produto)
        # self.btn_editar.pack(side="left", padx=10, pady=10)

        self.btn_excluir = ctk.CTkButton(self.frame_botoes, text="Excluir Selecionado", command=self.excluir_produto, fg_color="red", hover_color="#9B0000")
        self.btn_excluir.pack(side="right", padx=10, pady=10)

        self.protocol("WM_DELETE_WINDOW", self.fechar_janela)
        self.atualizar_tabela()

    def atualizar_tabela(self):
        for widget in self.frame_tabela.winfo_children():
            widget.destroy()

        # Adiciona nova coluna para Categoria
        ctk.CTkLabel(self.frame_tabela, text="Nome do Produto", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        ctk.CTkLabel(self.frame_tabela, text="Preço", font=ctk.CTkFont(weight="bold")).grid(row=0, column=1, padx=10, pady=5)
        ctk.CTkLabel(self.frame_tabela, text="Categoria", font=ctk.CTkFont(weight="bold")).grid(row=0, column=2, padx=10, pady=5)
        ctk.CTkLabel(self.frame_tabela, text="Sel.", font=ctk.CTkFont(weight="bold")).grid(row=0, column=3, padx=5, pady=5)

        self.produtos = gd.carregar_dados(gd.ARQUIVO_PRODUTOS)
        for i, produto in enumerate(self.produtos, start=1):
            ctk.CTkLabel(self.frame_tabela, text=produto['nome']).grid(row=i, column=0, padx=10, sticky="w")
            ctk.CTkLabel(self.frame_tabela, text=f"R$ {produto['preco']:.2f}").grid(row=i, column=1, padx=10)
            ctk.CTkLabel(self.frame_tabela, text=produto.get('categoria', 'N/A')).grid(row=i, column=2, padx=10)
            
            radio_btn = ctk.CTkRadioButton(self.frame_tabela, text="", variable=self.produto_selecionado_id, value=str(produto['id']))
            radio_btn.grid(row=i, column=3, padx=5, sticky="e")

    def adicionar_produto(self):
        dialog = DialogoProduto(self)
        novo_produto = dialog.get_produto()
        
        if novo_produto:
            self.produtos.append(novo_produto)
            gd.salvar_dados(gd.ARQUIVO_PRODUTOS, self.produtos)
            self.atualizar_tabela()

    def excluir_produto(self):
        # ... (método excluir_produto continua igual) ...
        id_selecionado = self.produto_selecionado_id.get()
        if not id_selecionado:
            messagebox.showwarning("Aviso", "Por favor, selecione um produto para excluir.")
            return

        confirmar = messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja excluir o produto com ID {id_selecionado}?")
        
        if confirmar:
            self.produtos = [p for p in self.produtos if str(p['id']) != id_selecionado]
            gd.salvar_dados(gd.ARQUIVO_PRODUTOS, self.produtos)
            self.produto_selecionado_id.set("")
            self.atualizar_tabela()
    
    def fechar_janela(self):
        self.master.atualizar_dropdown_produtos()
        self.destroy()