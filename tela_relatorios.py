import customtkinter as ctk
from collections import defaultdict
from tkcalendar import DateEntry
from datetime import datetime, date
import gerenciador_dados as gd

class TelaRelatorios(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Relatório de Vendas Avançado")
        self.geometry("950x700") # Aumentado para o novo quadro
        self.transient(master)
        self.grab_set()

        self.todas_as_vendas = gd.carregar_dados(gd.ARQUIVO_VENDAS)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.frame_filtros = ctk.CTkFrame(self)
        self.frame_filtros.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self._criar_widgets_de_filtro()

        self.frame_resultados = ctk.CTkFrame(self)
        self.frame_resultados.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.frame_resultados.grid_columnconfigure((0, 1), weight=1)
        self._criar_widgets_de_resultados()

        self._configurar_datas_padrao()
        self._aplicar_filtros()
        self._calcular_e_atualizar_resumo_hoje() # <-- NOVO: Chamada para o resumo do dia

    def _criar_widgets_de_filtro(self):
        # Frame para os filtros de data e botões
        frame_controles_principais = ctk.CTkFrame(self.frame_filtros)
        frame_controles_principais.grid(row=0, column=0, padx=5, pady=5, sticky="ns")
        
        ctk.CTkLabel(frame_controles_principais, text="De:").grid(row=0, column=0, padx=5, pady=5)
        self.cal_inicio = DateEntry(frame_controles_principais, date_pattern='dd/mm/yyyy', background='#2B2B2B', foreground='white', borderwidth=2, headersbackground='#2B2B2B', normalbackground='#2B2B2B')
        self.cal_inicio.grid(row=0, column=1, padx=5, pady=5)

        ctk.CTkLabel(frame_controles_principais, text="Até:").grid(row=1, column=0, padx=5, pady=5)
        self.cal_fim = DateEntry(frame_controles_principais, date_pattern='dd/mm/yyyy', background='#2B2B2B', foreground='white', borderwidth=2, headersbackground='#2B2B2B', normalbackground='#2B2B2B')
        self.cal_fim.grid(row=1, column=1, padx=5, pady=5)

        btn_aplicar = ctk.CTkButton(frame_controles_principais, text="Aplicar Filtros", command=self._aplicar_filtros)
        btn_aplicar.grid(row=2, column=0, pady=10)

        btn_limpar = ctk.CTkButton(frame_controles_principais, text="Limpar Filtros", command=self._limpar_filtros)
        btn_limpar.grid(row=2, column=1, pady=10)

        # Frame para os filtros de categoria
        categorias_frame = ctk.CTkScrollableFrame(self.frame_filtros, label_text="Categorias")
        categorias_frame.grid(row=0, column=1, padx=10, pady=5, sticky="ns")
        
        categorias_unicas = sorted(list(set(item.get('categoria', 'N/A') for venda in self.todas_as_vendas for item in venda.get('itens', []))))
        self.vars_categorias = {}
        for i, categoria in enumerate(categorias_unicas):
            var = ctk.StringVar(value="")
            cb = ctk.CTkCheckBox(categorias_frame, text=categoria, variable=var, onvalue=categoria, offvalue="")
            cb.pack(anchor="w", padx=5)
            self.vars_categorias[categoria] = var

        ### NOVO: QUADRO PARA O RESUMO DO DIA ###
        frame_resumo_hoje = ctk.CTkFrame(self.frame_filtros, border_width=1)
        frame_resumo_hoje.grid(row=0, column=2, padx=10, pady=5, sticky="ns")
        
        ctk.CTkLabel(frame_resumo_hoje, text="Vendas de Hoje", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(5,10), padx=20)
        self.label_hoje_faturamento = ctk.CTkLabel(frame_resumo_hoje, text="Faturamento: R$ 0.00", font=ctk.CTkFont(size=12))
        self.label_hoje_faturamento.pack(anchor="w", padx=20)
        self.label_hoje_vendas = ctk.CTkLabel(frame_resumo_hoje, text="Nº de Vendas: 0", font=ctk.CTkFont(size=12))
        self.label_hoje_vendas.pack(anchor="w", padx=20, pady=(0, 10))

        # Faz o quadro de resumo expandir se houver espaço
        self.frame_filtros.grid_columnconfigure(2, weight=1)

    ### NOVO: MÉTODO PARA O RESUMO DO DIA ###
    def _calcular_e_atualizar_resumo_hoje(self):
        hoje = date.today()
        faturamento_hoje = 0.0
        num_vendas_hoje = 0

        for venda in self.todas_as_vendas:
            try:
                data_venda = datetime.fromisoformat(venda['data_hora']).date()
                if data_venda == hoje:
                    faturamento_hoje += venda.get('total_venda', 0)
                    num_vendas_hoje += 1
            except (ValueError, TypeError):
                continue
        
        self.label_hoje_faturamento.configure(text=f"Faturamento: R$ {faturamento_hoje:.2f}")
        self.label_hoje_vendas.configure(text=f"Nº de Vendas: {num_vendas_hoje}")

    # ... O resto dos métodos continua igual ...
    def _configurar_datas_padrao(self):
        if not self.todas_as_vendas: return
        datas_vendas = [datetime.fromisoformat(venda['data_hora']).date() for venda in self.todas_as_vendas if 'data_hora' in venda]
        if datas_vendas:
            self.cal_inicio.set_date(min(datas_vendas))
            self.cal_fim.set_date(max(datas_vendas))

    def _criar_widgets_de_resultados(self):
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
        data_inicio = self.cal_inicio.get_date()
        data_fim = self.cal_fim.get_date()
        categorias_selecionadas = [var.get() for var in self.vars_categorias.values() if var.get()]
        vendas_filtradas = []
        for venda in self.todas_as_vendas:
            try:
                data_venda = datetime.fromisoformat(venda['data_hora']).date()
                if data_inicio <= data_venda <= data_fim:
                    itens_filtrados = [item for item in venda['itens'] if not categorias_selecionadas or item.get('categoria', 'N/A') in categorias_selecionadas]
                    if itens_filtrados:
                        venda_copia = venda.copy()
                        venda_copia['itens'] = itens_filtrados
                        vendas_filtradas.append(venda_copia)
            except (ValueError, TypeError): continue
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
        for frame in [self.frame_cat, self.frame_prod, self.frame_hora]:
            for widget in frame.winfo_children(): widget.destroy()
        self.label_faturamento_valor.configure(text=f"R$ {faturamento:.2f}")
        if not faturamento_cat: ctk.CTkLabel(self.frame_cat, text="Nenhum dado para o período.").pack()
        for cat, total in sorted(faturamento_cat.items()): ctk.CTkLabel(self.frame_cat, text=f"{cat}: R$ {total:.2f}").pack(anchor="w", padx=5)
        if not produtos_vendidos: ctk.CTkLabel(self.frame_prod, text="Nenhum dado para o período.").pack()
        for prod, qtd in sorted(produtos_vendidos.items(), key=lambda item: item[1], reverse=True): ctk.CTkLabel(self.frame_prod, text=f"{qtd}x - {prod}").pack(anchor="w", padx=5)
        if not vendas_hora: ctk.CTkLabel(self.frame_hora, text="Nenhum dado para o período.").pack()
        for hora, total in sorted(vendas_hora.items()): ctk.CTkLabel(self.frame_hora, text=f"{hora:02d}h - {hora+1:02d}h: R$ {total:.2f}").pack(anchor="w", padx=5)

    def _limpar_filtros(self):
        for var in self.vars_categorias.values(): var.set("")
        self._configurar_datas_padrao()
        self._aplicar_filtros()