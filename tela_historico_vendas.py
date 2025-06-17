import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
import gerenciador_dados as gd

class TelaHistoricoVendas(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Histórico e Gerenciamento de Vendas")
        self.geometry("750x500")
        self.transient(master)
        self.grab_set()

        # Variáveis
        self.todas_as_vendas = gd.carregar_dados(gd.ARQUIVO_VENDAS)
        self.venda_selecionada_id = ctk.StringVar()

        # --- Estrutura ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Frame da lista de vendas
        self.frame_lista = ctk.CTkScrollableFrame(self, label_text="Vendas Registradas")
        self.frame_lista.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.frame_lista.grid_columnconfigure(1, weight=1)

        # Botão de Exclusão
        self.btn_excluir = ctk.CTkButton(self, text="Excluir Venda Selecionada", command=self.excluir_venda, fg_color="red", hover_color="#9B0000")
        self.btn_excluir.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.atualizar_lista_vendas()

    def atualizar_lista_vendas(self):
        # Limpa a lista antiga
        for widget in self.frame_lista.winfo_children():
            widget.destroy()
        
        # Recarrega os dados do arquivo
        self.todas_as_vendas = gd.carregar_dados(gd.ARQUIVO_VENDAS)

        # Adiciona cabeçalhos
        ctk.CTkLabel(self.frame_lista, text="Data e Hora", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        ctk.CTkLabel(self.frame_lista, text="ID da Venda", font=ctk.CTkFont(weight="bold")).grid(row=0, column=1, padx=10, pady=5, sticky="w")
        ctk.CTkLabel(self.frame_lista, text="Total", font=ctk.CTkFont(weight="bold")).grid(row=0, column=2, padx=10, pady=5, sticky="w")
        ctk.CTkLabel(self.frame_lista, text="Sel.", font=ctk.CTkFont(weight="bold")).grid(row=0, column=3, padx=5, pady=5, sticky="e")

        # Preenche a lista com as vendas
        # Ordena as vendas da mais recente para a mais antiga
        vendas_ordenadas = sorted(self.todas_as_vendas, key=lambda v: v['data_hora'], reverse=True)

        for i, venda in enumerate(vendas_ordenadas, start=1):
            try:
                # Formata a data para melhor visualização
                data_obj = datetime.fromisoformat(venda['data_hora'])
                data_formatada = data_obj.strftime("%d/%m/%Y %H:%M:%S")
            except ValueError:
                data_formatada = venda['data_hora']

            total_venda = venda.get('total_venda', 0.0)
            id_venda = venda.get('id_venda', 'N/A')

            ctk.CTkLabel(self.frame_lista, text=data_formatada).grid(row=i, column=0, padx=10, pady=5, sticky="w")
            ctk.CTkLabel(self.frame_lista, text=id_venda).grid(row=i, column=1, padx=10, pady=5, sticky="w")
            ctk.CTkLabel(self.frame_lista, text=f"R$ {total_venda:.2f}").grid(row=i, column=2, padx=10, pady=5, sticky="w")
            
            radio_btn = ctk.CTkRadioButton(self.frame_lista, text="", variable=self.venda_selecionada_id, value=id_venda)
            radio_btn.grid(row=i, column=3, padx=5, pady=5, sticky="e")

    def excluir_venda(self):
        id_selecionado = self.venda_selecionada_id.get()
        if not id_selecionado:
            messagebox.showwarning("Nenhuma Venda Selecionada", "Por favor, selecione uma venda da lista para excluir.", parent=self)
            return

        # ETAPA DE SEGURANÇA: Confirmação do usuário
        confirmar = messagebox.askyesno(
            "Confirmar Exclusão", 
            f"Você tem certeza absoluta que deseja excluir a venda com ID:\n{id_selecionado}\n\nEsta ação não pode ser desfeita.",
            icon='warning',
            parent=self
        )
        
        if confirmar:
            # Filtra a lista, mantendo todas as vendas EXCETO a selecionada
            vendas_atualizadas = [venda for venda in self.todas_as_vendas if venda['id_venda'] != id_selecionado]
            
            # Salva a nova lista (sem a venda excluída) no arquivo
            gd.salvar_dados(gd.ARQUIVO_VENDAS, vendas_atualizadas)
            
            # Limpa a seleção e atualiza a interface
            self.venda_selecionada_id.set("")
            self.atualizar_lista_vendas()
            messagebox.showinfo("Sucesso", "A venda foi excluída com sucesso.", parent=self)