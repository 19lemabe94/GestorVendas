import customtkinter as ctk
from datetime import datetime
import gerenciador_dados as gd

# --- Configurações Iniciais ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sistema de Comanda Eletrônica")
        self.geometry("800x600")

        # Variáveis
        self.produtos = gd.carregar_dados(gd.ARQUIVO_PRODUTOS)
        self.comanda_atual = []
        self.total_atual = 0.0

        # --- Layout Principal ---
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Frame de Controles (Esquerda) ---
        self.frame_controles = ctk.CTkFrame(self, width=250)
        self.frame_controles.grid(row=0, column=0, rowspan=2, padx=10, pady=10, sticky="nsew")

        self.label_produto = ctk.CTkLabel(self.frame_controles, text="Produto:")
        self.label_produto.pack(padx=10, pady=(10, 0))

        # Dropdown para selecionar produtos
        nomes_produtos = [p['nome'] for p in self.produtos] if self.produtos else ["Nenhum produto"]
        self.produto_selecionado = ctk.StringVar(value=nomes_produtos[0])
        self.option_menu_produtos = ctk.CTkOptionMenu(self.frame_controles, variable=self.produto_selecionado, values=nomes_produtos)
        self.option_menu_produtos.pack(padx=10, pady=5)

        self.label_qtd = ctk.CTkLabel(self.frame_controles, text="Quantidade:")
        self.label_qtd.pack(padx=10, pady=(10, 0))

        self.entry_qtd = ctk.CTkEntry(self.frame_controles, placeholder_text="1")
        self.entry_qtd.pack(padx=10, pady=5)

        self.btn_adicionar = ctk.CTkButton(self.frame_controles, text="Adicionar à Comanda", command=self.adicionar_item)
        self.btn_adicionar.pack(padx=10, pady=20)
        
        # --- Botão para gerenciar produtos (você criará essa tela) ---
        self.btn_gerenciar_produtos = ctk.CTkButton(self.frame_controles, text="Gerenciar Produtos")
        self.btn_gerenciar_produtos.pack(side="bottom", padx=10, pady=10)


        # --- Frame da Comanda (Direita) ---
        self.frame_comanda = ctk.CTkFrame(self)
        self.frame_comanda.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.frame_comanda.grid_columnconfigure(0, weight=1)
        self.frame_comanda.grid_rowconfigure(0, weight=1)
        
        self.textbox_comanda = ctk.CTkTextbox(self.frame_comanda, font=("Consolas", 14))
        self.textbox_comanda.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.textbox_comanda.insert("0.0", "--- COMANDA ---\n")
        self.textbox_comanda.configure(state="disabled") # Para não ser editável pelo usuário

        self.label_total = ctk.CTkLabel(self.frame_comanda, text="Total: R$ 0.00", font=("Arial", 20, "bold"))
        self.label_total.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        # --- Frame de Ações (Abaixo da Comanda) ---
        self.btn_finalizar = ctk.CTkButton(self, text="Finalizar Venda", height=40, command=self.finalizar_venda)
        self.btn_finalizar.grid(row=1, column=1, padx=10, pady=10, sticky="sew")


    def adicionar_item(self):
        nome_produto = self.produto_selecionado.get()
        try:
            quantidade = int(self.entry_qtd.get() or 1) # Pega 1 se o campo estiver vazio
        except ValueError:
            # Aqui você pode mostrar uma mensagem de erro
            print("Quantidade inválida!")
            return

        produto_encontrado = next((p for p in self.produtos if p['nome'] == nome_produto), None)

        if produto_encontrado:
            item = {
                "id_produto": produto_encontrado['id'],
                "nome": produto_encontrado['nome'],
                "quantidade": quantidade,
                "preco_unitario": produto_encontrado['preco']
            }
            self.comanda_atual.append(item)
            self.atualizar_display_comanda()

    def atualizar_display_comanda(self):
        self.textbox_comanda.configure(state="normal")
        self.textbox_comanda.delete("0.0", "end")
        
        header = f"{'--- COMANDA ELETRÔNICA ---':^45}\n"
        header += f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S'):^45}\n"
        header += "="*45 + "\n"
        header += f"{'Qtd':<4} {'Produto':<25} {'Preço Unit.':>12}\n"
        header += "-"*45 + "\n"
        self.textbox_comanda.insert("0.0", header)

        self.total_atual = 0.0
        for item in self.comanda_atual:
            subtotal = item['quantidade'] * item['preco_unitario']
            self.total_atual += subtotal
            linha = f"{item['quantidade']:<4d} {item['nome']:<25} R$ {item['preco_unitario']:>10.2f}\n"
            self.textbox_comanda.insert("end", linha)
        
        self.textbox_comanda.configure(state="disabled")
        self.label_total.configure(text=f"Total: R$ {self.total_atual:.2f}")

    def finalizar_venda(self):
        if not self.comanda_atual:
            print("Comanda vazia!")
            return
            
        vendas = gd.carregar_dados(gd.ARQUIVO_VENDAS)
        
        nova_venda = {
            "id_venda": datetime.now().strftime("%Y%m%d%H%M%S%f"),
            "data_hora": datetime.now().isoformat(),
            "itens": self.comanda_atual,
            "total_venda": self.total_atual
        }
        
        vendas.append(nova_venda)
        gd.salvar_dados(gd.ARQUIVO_VENDAS, vendas)
        
        # Limpar para a próxima venda
        self.comanda_atual = []
        self.total_atual = 0.0
        self.atualizar_display_comanda()
        # Adicionar uma mensagem de sucesso para o usuário
        print("Venda finalizada e salva com sucesso!")


if __name__ == "__main__":
    app = App()
    app.mainloop()