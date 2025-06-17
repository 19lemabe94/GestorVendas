# tela_historico_vendas.py
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
import gerenciador_dados as gd

class TelaHistoricoVendas(ctk.CTkToplevel):
    """
    Janela para visualizar, gerenciar e excluir o histórico de vendas registradas.
    """
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Histórico e Gerenciamento de Vendas")
        self.geometry("750x500")
        self.resizable(False, False)
        self.transient(master)  # Mantém a janela na frente da principal
        self.grab_set()         # Impede interação com a janela principal

        # --- Variáveis de Estado ---
        self.todas_as_vendas = []
        self.venda_selecionada_id = ctk.StringVar()

        # --- Estrutura da Janela ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Frame principal com a lista de vendas
        self.frame_lista = ctk.CTkScrollableFrame(self, label_text="Vendas Registradas")
        self.frame_lista.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.frame_lista.grid_columnconfigure(1, weight=1)  # Coluna do ID expande

        # Botão de Exclusão
        self.btn_excluir = ctk.CTkButton(self, text="Excluir Venda Selecionada", 
                                         command=self.excluir_venda, 
                                         fg_color="red", hover_color="#9B0000")
        self.btn_excluir.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        # Carrega os dados e popula a tabela na inicialização
        self.atualizar_lista_vendas()

    def atualizar_lista_vendas(self):
        """
        Limpa a tabela atual, recarrega os dados do arquivo JSON
        e recria a lista de vendas na tela.
        """
        # 1. Limpa todos os widgets antigos da lista
        for widget in self.frame_lista.winfo_children():
            widget.destroy()
        
        # 2. Recarrega os dados do arquivo para garantir que estão atualizados
        self.todas_as_vendas = gd.carregar_dados(gd.ARQUIVO_VENDAS)

        # 3. Adiciona os cabeçalhos das colunas
        headers = ["Data e Hora", "ID da Venda", "Pagamento", "Total", "Sel."]
        column_weights = [0, 1, 0, 0, 0] # Define qual coluna expande

        for i, header in enumerate(headers):
            self.frame_lista.grid_columnconfigure(i, weight=column_weights[i])
            ctk.CTkLabel(self.frame_lista, text=header, font=ctk.CTkFont(weight="bold")).grid(row=0, column=i, padx=10, pady=5, sticky="w")

        # 4. Ordena as vendas da mais recente para a mais antiga (melhor UX)
        vendas_ordenadas = sorted(self.todas_as_vendas, key=lambda v: v.get('data_hora', ''), reverse=True)

        # 5. Preenche a lista com as vendas
        for i, venda in enumerate(vendas_ordenadas, start=1):
            # Formatação segura da data
            try:
                data_obj = datetime.fromisoformat(venda.get('data_hora', ''))
                data_formatada = data_obj.strftime("%d/%m/%Y %H:%M:%S")
            except (ValueError, TypeError):
                data_formatada = venda.get('data_hora', 'Data Inválida')

            # Obtenção segura dos dados com valores padrão
            total_venda = venda.get('total_venda', 0.0)
            id_venda = venda.get('id_venda', 'N/A')
            metodo_pag = venda.get('metodo_pagamento', 'N/D')

            # Criação dos labels para cada coluna
            ctk.CTkLabel(self.frame_lista, text=data_formatada).grid(row=i, column=0, padx=10, pady=5, sticky="w")
            ctk.CTkLabel(self.frame_lista, text=id_venda, anchor="w").grid(row=i, column=1, padx=10, pady=5, sticky="ew")
            ctk.CTkLabel(self.frame_lista, text=metodo_pag).grid(row=i, column=2, padx=10, pady=5, sticky="w")
            ctk.CTkLabel(self.frame_lista, text=f"R$ {total_venda:.2f}").grid(row=i, column=3, padx=10, pady=5, sticky="w")
            
            # Botão de rádio para seleção
            radio_btn = ctk.CTkRadioButton(self.frame_lista, text="", variable=self.venda_selecionada_id, value=id_venda)
            radio_btn.grid(row=i, column=4, padx=5, pady=5, sticky="e")

    def excluir_venda(self):
        """
        Exclui a venda selecionada na lista, após confirmação do usuário.
        """
        id_selecionado = self.venda_selecionada_id.get()
        if not id_selecionado:
            messagebox.showwarning("Nenhuma Venda Selecionada", 
                                   "Por favor, selecione uma venda da lista para excluir.", 
                                   parent=self)
            return

        # Etapa de Segurança Crítica: Confirmação do usuário
        confirmar = messagebox.askyesno(
            "Confirmar Exclusão", 
            f"Você tem certeza absoluta que deseja excluir a venda com ID:\n{id_selecionado}\n\nEsta ação não pode ser desfeita.",
            icon='warning', # Ícone de aviso
            parent=self
        )
        
        if confirmar:
            # 1. Filtra a lista, mantendo todas as vendas EXCETO a selecionada
            vendas_atualizadas = [venda for venda in self.todas_as_vendas if venda['id_venda'] != id_selecionado]
            
            # 2. Salva a nova lista (sem a venda excluída) de volta no arquivo
            gd.salvar_dados(gd.ARQUIVO_VENDAS, vendas_atualizadas)
            
            # 3. Limpa a variável de seleção e atualiza a interface
            self.venda_selecionada_id.set("")
            self.atualizar_lista_vendas()
            messagebox.showinfo("Sucesso", "A venda foi excluída com sucesso.", parent=self)