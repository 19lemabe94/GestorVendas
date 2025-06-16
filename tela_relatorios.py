import customtkinter as ctk
from collections import defaultdict
from tkcalendar import DateEntry
from datetime import datetime, date
import gerenciador_dados as gd

class TelaRelatorios(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Relatório de Vendas Avançado")
        self.geometry("800x700")
        self.transient(master)
        self.grab_set()

        # Carregar todos os dados uma vez
        self.todas_as_vendas = gd.carregar_dados(gd.ARQUIVO_VENDAS)
        
        # --- Estrutura principal da tela ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # --- Frame de Filtros ---
        self.frame_filtros = ctk.CTkFrame(self)
        self.frame_filtros.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self._criar_widgets_de_filtro()

        # --- Frame de Resultados ---
        self.frame_resultados = ctk.CTkFrame(self)
        self.frame_resultados.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.frame_resultados.grid_columnconfigure((0, 1), weight=1)
        self._criar_widgets_de_resultados()

        # ### ALTERAÇÃO PRINCIPAL ###
        # Configurar as datas padrão e aplicar o filtro inicial
        self._configurar_datas_padrao()
        self._aplicar_filtros()

    def _criar_widgets_de_filtro(self):
        # Filtros de Data
        ctk.CTkLabel(self.frame_filtros, text="De:").grid(row=0, column=0, padx=5, pady=5)
        self.cal_inicio = DateEntry(self.frame_filtros, date_pattern='dd/mm/yyyy', background='#2B2B2B', foreground='white', borderwidth=2, headersbackground='#2B2B2B', normalbackground='#2B2B2B')
        self.cal_inicio.grid(row=0, column=1, padx=5, pady=5)

        ctk.CTkLabel(self.frame_filtros, text="Até:").grid(row=0, column=2, padx=5, pady=5)
        self.cal_fim = DateEntry(self.frame_filtros, date_pattern='dd/mm/yyyy', background='#2B2B2B', foreground='white', borderwidth=2, headersbackground='#2B2B2B', normalbackground='#2B2B2B')
        self.cal_fim.grid(row=0, column=3, padx=5, pady=5)

        # Filtros de Categoria
        categorias_frame = ctk.CTkScrollableFrame(self.frame_filtros, label_text="Categorias")
        categorias_frame.grid(row=0, column=4, rowspan=2, padx=10, pady=5, sticky="ns")
        
        # Garante que a lista não quebre se não houver vendas ou categorias
        categorias_unicas = sorted(list(set(item.get('categoria', 'N/A') for venda in self.todas_as_vendas for item in venda.get('itens', []))))
        self.vars_categorias = {}
        for i, categoria in enumerate(categorias_unicas):
            var = ctk.StringVar(value="") # Inicia desmarcado
            cb = ctk.CTkCheckBox(categorias_frame, text=categoria, variable=var, onvalue=categoria, offvalue="")
            cb.pack(anchor="w", padx=5)
            self.vars_categorias[categoria] = var

        # Botões de Ação
        btn_aplicar = ctk.CTkButton(self.frame_filtros, text="Aplicar Filtros", command=self._aplicar_filtros)
        btn_aplicar.grid(row=1, column=0, columnspan=2, pady=10)

        btn_limpar = ctk.CTkButton(self.frame_filtros, text="Limpar Filtros", command=self._limpar_filtros)
        btn_limpar.grid(row=1, column=2, columnspan=2, pady=10)

    def _configurar_datas_padrao(self):
        # ### NOVO MÉTODO ###
        # Encontra a primeira e a última data de venda para definir o período padrão
        if not self.todas_as_vendas:
            return # Não faz nada se não houver vendas

        datas_vendas = [datetime.fromisoformat(venda['data_hora']).date() for venda in self.todas_as_vendas if 'data_hora' in venda]
        
        if datas_vendas:
            data_minima = min(datas_vendas)
            data_maxima = max(datas_vendas)
            self.cal_inicio.set_date(data_minima)
            self.cal_fim.set_date(data_maxima)

    def _criar_widgets_de_resultados(self):
        # ... este método não precisa de alterações ...
        self.label_faturamento_titulo = ctk.CTkLabel(self.frame_resultados, text="Faturamento Total Filtrado", font=ctk.CTkFont(size=16, weight="bold"))
        self.label_faturamento_titulo.grid(row=0, column=0, columnspan=2, pady=(10,5))
        self.label_faturamento_valor = ctk.CTkLabel(self.frame_resultados, text="R$ 0.00", font=ctk.CTkFont(size=20))
        self.label_faturamento_valor.grid(row=1, column=0, columnspan=2, pady=(0, 20))

        self.frame_cat = ctk.CTkScrollableFrame(self.frame_resultados, label_text="Faturamento por Categoria")
        self.frame_cat.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")

        self.frame_prod = ctk.CTkScrollableFrame(self.frame_resultados, label_text="Top Produtos Vendidos")
        self.frame_prod.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")

        self.frame_hora = ctk.CTkScrollableFrame(self.frame_resultados, label_text="Vendas por Hora")
        self.frame_hora.grid(row=2, column=1, rowspan=2, padx=5, pady=5, sticky="nsew")
        
        self.frame_resultados.grid_rowconfigure((2, 3), weight=1)

    def _aplicar_filtros(self):
        # ... este método não precisa de alterações na sua lógica principal ...
        data_inicio = self.cal_inicio.get_date()
        data_fim = self.cal_fim.get_date()
        categorias_selecionadas = [var.get() for var in self.vars_categorias.values() if var.get()]

        vendas_filtradas = []
        for venda in self.todas_as_vendas:
            try:
                data_venda = datetime.fromisoformat(venda['data_hora']).date()
                if data_inicio <= data_venda <= data_fim:
                    itens_filtrados = [
                        item for item in venda['itens'] 
                        if not categorias_selecionadas or item.get('categoria', 'N/A') in categorias_selecionadas
                    ]
                    if itens_filtrados:
                        venda_copia = venda.copy()
                        venda_copia['itens'] = itens_filtrados
                        vendas_filtradas.append(venda_copia)
            except (ValueError, TypeError):
                continue

        faturamento_total = 0.0
        faturamento_por_categoria = defaultdict(float)
        produtos_vendidos = defaultdict(int)
        vendas_por_hora = defaultdict(float)

        for venda in vendas_filtradas:
            hora_venda = datetime.fromisoformat(venda['data_hora']).hour
            for item in venda['itens']:
                subtotal = item['quantidade'] * item['preco_unitario']
                faturamento_total += subtotal
                faturamento_por_categoria[item.get('categoria', 'N/A')] += subtotal
                produtos_vendidos[item['nome']] += item['quantidade']
                vendas_por_hora[hora_venda] += subtotal

        self._atualizar_ui_resultados(faturamento_total, faturamento_por_categoria, produtos_vendidos, vendas_por_hora)
    
    def _atualizar_ui_resultados(self, faturamento, faturamento_cat, produtos_vendidos, vendas_hora):
        # ... este método não precisa de alterações ...
        for frame in [self.frame_cat, self.frame_prod, self.frame_hora]:
            for widget in frame.winfo_children():
                widget.destroy()

        self.label_faturamento_valor.configure(text=f"R$ {faturamento:.2f}")

        if not faturamento_cat:
            ctk.CTkLabel(self.frame_cat, text="Nenhum dado para o período.").pack()
        for cat, total in sorted(faturamento_cat.items()):
            ctk.CTkLabel(self.frame_cat, text=f"{cat}: R$ {total:.2f}").pack(anchor="w", padx=5)

        if not produtos_vendidos:
            ctk.CTkLabel(self.frame_prod, text="Nenhum dado para o período.").pack()
        for prod, qtd in sorted(produtos_vendidos.items(), key=lambda item: item[1], reverse=True):
            ctk.CTkLabel(self.frame_prod, text=f"{qtd}x - {prod}").pack(anchor="w", padx=5)
        
        if not vendas_hora:
            ctk.CTkLabel(self.frame_hora, text="Nenhum dado para o período.").pack()
        for hora, total in sorted(vendas_hora.items()):
            ctk.CTkLabel(self.frame_hora, text=f"{hora:02d}h - {hora+1:02d}h: R$ {total:.2f}").pack(anchor="w", padx=5)

    def _limpar_filtros(self):
        # Desmarcar todas as checkboxes
        for var in self.vars_categorias.values():
            var.set("")
        # Restaurar datas padrão e aplicar
        self._configurar_datas_padrao()
        self._aplicar_filtros()