import customtkinter as ctk
from datetime import datetime
import gerenciador_dados as gd
from tela_produtos import TelaGerenciamentoProdutos 
from tela_relatorios import TelaRelatorios
from tela_historico_vendas import TelaHistoricoVendas

### NOVO: CLASSE PARA O DIÁLOGO DE PAGAMENTO ###
class DialogoPagamento(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Forma de Pagamento")
        self.geometry("300x150")
        self.transient(master)
        self.grab_set()
        self.resizable(False, False)

        self.metodo_selecionado = None
        self.pagamento_var = ctk.StringVar(value="")

        self.label = ctk.CTkLabel(self, text="Selecione o método de pagamento:", font=ctk.CTkFont(size=14))
        self.label.pack(pady=10)

        self.radio_dinheiro = ctk.CTkRadioButton(self, text="Dinheiro", variable=self.pagamento_var, value="Dinheiro")
        self.radio_dinheiro.pack(anchor="w", padx=40, pady=5)
        
        self.radio_cartao = ctk.CTkRadioButton(self, text="Cartão", variable=self.pagamento_var, value="Cartão")
        self.radio_cartao.pack(anchor="w", padx=40, pady=5)

        self.btn_confirmar = ctk.CTkButton(self, text="Confirmar Venda", command=self.confirmar)
        self.btn_confirmar.pack(pady=10)

    def confirmar(self):
        if self.pagamento_var.get():
            self.metodo_selecionado = self.pagamento_var.get()
            self.destroy()
        else:
            # Opcional: Adicionar um aviso se nada for selecionado
            from tkinter import messagebox
            messagebox.showwarning("Seleção Obrigatória", "Por favor, selecione um método de pagamento.", parent=self)

    def get_metodo(self):
        # Faz a janela principal esperar até que esta seja fechada
        self.wait_window()
        return self.metodo_selecionado


class App(ctk.CTk):
    def __init__(self):
        # ... O __init__ continua igual até o final ...
        super().__init__()
        self.title("Sistema de Comanda Eletrônica")
        self.geometry("800x600")
        self.produtos = gd.carregar_dados(gd.ARQUIVO_PRODUTOS)
        self.comanda_atual = []
        self.total_atual = 0.0
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.frame_controles = ctk.CTkFrame(self, width=250)
        self.frame_controles.grid(row=0, column=0, rowspan=2, padx=10, pady=10, sticky="nsew")
        self.label_produto = ctk.CTkLabel(self.frame_controles, text="Produto:")
        self.label_produto.pack(padx=10, pady=(10, 0))
        nomes_produtos = [p['nome'] for p in self.produtos] if self.produtos else ["Nenhum produto"]
        valor_inicial_dropdown = nomes_produtos[0] if nomes_produtos else ""
        self.produto_selecionado = ctk.StringVar(value=valor_inicial_dropdown)
        self.option_menu_produtos = ctk.CTkOptionMenu(self.frame_controles, variable=self.produto_selecionado, values=nomes_produtos)
        self.option_menu_produtos.pack(padx=10, pady=5)
        self.label_qtd = ctk.CTkLabel(self.frame_controles, text="Quantidade:")
        self.label_qtd.pack(padx=10, pady=(10, 0))
        self.entry_qtd = ctk.CTkEntry(self.frame_controles, placeholder_text="1")
        self.entry_qtd.pack(padx=10, pady=5)
        self.btn_adicionar = ctk.CTkButton(self.frame_controles, text="Adicionar à Comanda", command=self.adicionar_item)
        self.btn_adicionar.pack(padx=10, pady=10)
        self.btn_limpar = ctk.CTkButton(self.frame_controles, text="Limpar Comanda", command=self.limpar_comanda, fg_color="#585858", hover_color="#686868")
        self.btn_limpar.pack(padx=10, pady=5)
        self.frame_gerenciamento = ctk.CTkFrame(self.frame_controles)
        self.frame_gerenciamento.pack(side="bottom", fill="x", pady=10)
        self.btn_relatorios = ctk.CTkButton(self.frame_gerenciamento, text="Relatórios de Vendas", command=self.abrir_tela_relatorios)
        self.btn_relatorios.pack(fill="x", padx=10, pady=5)
        self.btn_historico = ctk.CTkButton(self.frame_gerenciamento, text="Histórico de Vendas", command=self.abrir_tela_historico)
        self.btn_historico.pack(fill="x", padx=10, pady=5)
        self.btn_gerenciar_produtos = ctk.CTkButton(self.frame_gerenciamento, text="Gerenciar Produtos", command=self.abrir_tela_produtos)
        self.btn_gerenciar_produtos.pack(fill="x", padx=10, pady=5)
        self.frame_comanda = ctk.CTkFrame(self)
        self.frame_comanda.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.frame_comanda.grid_columnconfigure(0, weight=1)
        self.frame_comanda.grid_rowconfigure(0, weight=1)
        self.textbox_comanda = ctk.CTkTextbox(self.frame_comanda, font=("Consolas", 14))
        self.textbox_comanda.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.textbox_comanda.insert("0.0", "--- COMANDA ---\n")
        self.textbox_comanda.configure(state="disabled")
        self.label_total = ctk.CTkLabel(self.frame_comanda, text="Total: R$ 0.00", font=("Arial", 20, "bold"))
        self.label_total.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.btn_finalizar = ctk.CTkButton(self, text="Finalizar Venda", height=40, command=self.finalizar_venda)
        self.btn_finalizar.grid(row=1, column=1, padx=10, pady=10, sticky="sew")

    ### MÉTODO FINALIZAR_VENDA TOTALMENTE ALTERADO ###
    def finalizar_venda(self):
        if not self.comanda_atual: 
            print("Comanda vazia, não há nada para finalizar.")
            return

        # 1. Abrir o diálogo e esperar pela escolha do usuário
        dialog = DialogoPagamento(self)
        metodo_pagamento = dialog.get_metodo() # Isso vai pausar a execução aqui

        # 2. Se um método foi escolhido (usuário não fechou a janela), continuar
        if metodo_pagamento:
            vendas = gd.carregar_dados(gd.ARQUIVO_VENDAS)
            
            nova_venda = {
                "id_venda": datetime.now().strftime("%Y%m%d%H%M%S%f"),
                "data_hora": datetime.now().isoformat(),
                "itens": self.comanda_atual,
                "total_venda": self.total_atual,
                "metodo_pagamento": metodo_pagamento # Adiciona a informação
            }
            
            vendas.append(nova_venda)
            gd.salvar_dados(gd.ARQUIVO_VENDAS, vendas)
            
            self.limpar_comanda()
            print(f"Venda finalizada com {metodo_pagamento} e salva com sucesso!")
        else:
            print("Finalização de venda cancelada pelo usuário.")

    # ... O resto da classe App não muda ...
    def abrir_tela_produtos(self):
        if hasattr(self, 'tela_produtos_aberta') and self.tela_produtos_aberta.winfo_exists(): self.tela_produtos_aberta.focus(); return
        self.tela_produtos_aberta = TelaGerenciamentoProdutos(master=self)
        self.tela_produtos_aberta.grab_set()
    def abrir_tela_relatorios(self):
        if hasattr(self, 'tela_relatorios_aberta') and self.tela_relatorios_aberta.winfo_exists(): self.tela_relatorios_aberta.focus(); return
        self.tela_relatorios_aberta = TelaRelatorios(master=self)
        self.tela_relatorios_aberta.grab_set()
    def abrir_tela_historico(self):
        if hasattr(self, 'tela_historico_aberta') and self.tela_historico_aberta.winfo_exists(): self.tela_historico_aberta.focus(); return
        self.tela_historico_aberta = TelaHistoricoVendas(master=self)
        self.tela_historico_aberta.grab_set()
    def limpar_comanda(self):
        self.comanda_atual = []
        self.total_atual = 0.0
        self.entry_qtd.delete(0, 'end')
        self.atualizar_display_comanda()
        print("Comanda limpa.")
    def atualizar_dropdown_produtos(self):
        self.produtos = gd.carregar_dados(gd.ARQUIVO_PRODUTOS)
        nomes_produtos = [p['nome'] for p in self.produtos] if self.produtos else ["Nenhum produto"]
        valor_padrao = nomes_produtos[0] if nomes_produtos else ""
        self.produto_selecionado.set(valor_padrao)
        self.option_menu_produtos.configure(values=nomes_produtos)
        print("Dropdown de produtos atualizado.")
    def adicionar_item(self):
        nome_produto = self.produto_selecionado.get()
        if not nome_produto or nome_produto == "Nenhum produto": return
        try: quantidade = int(self.entry_qtd.get() or 1)
        except ValueError: return
        produto_encontrado = next((p for p in self.produtos if p['nome'] == nome_produto), None)
        if produto_encontrado:
            item = {"id_produto": produto_encontrado['id'], "nome": produto_encontrado['nome'],"quantidade": quantidade, "preco_unitario": produto_encontrado['preco'], "categoria": produto_encontrado.get('categoria', 'Sem Categoria')}
            self.comanda_atual.append(item)
            self.atualizar_display_comanda()
    def atualizar_display_comanda(self):
        self.textbox_comanda.configure(state="normal")
        self.textbox_comanda.delete("0.0", "end")
        header = f"{'--- COMANDA ELETRÔNICA ---':^45}\n{datetime.now().strftime('%d/%m/%Y %H:%M:%S'):^45}\n{'='*45}\n{'Qtd':<4} {'Produto':<25} {'Preço Unit.':>12}\n{'-'*45}\n"
        self.textbox_comanda.insert("0.0", header)
        self.total_atual = 0.0
        if self.comanda_atual:
            for item in self.comanda_atual:
                subtotal = item['quantidade'] * item['preco_unitario']
                self.total_atual += subtotal
                linha = f"{item['quantidade']:<4d} {item['nome']:<25} R$ {item['preco_unitario']:>10.2f}\n"
                self.textbox_comanda.insert("end", linha)
        self.textbox_comanda.configure(state="disabled")
        self.label_total.configure(text=f"Total: R$ {self.total_atual:.2f}")


if __name__ == "__main__":
    app = App()
    app.mainloop()