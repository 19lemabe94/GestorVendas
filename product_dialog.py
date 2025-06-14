from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                             QPushButton, QTableWidget, QTableWidgetItem, QMessageBox,
                             QHeaderView)
from PyQt6.QtCore import Qt
from database_manager import DatabaseManager

class ProductDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Gerenciar Produtos")
        self.setGeometry(200, 200, 500, 400)

        # Inicializa o gerenciador do banco de dados
        self.db_manager = DatabaseManager()

        # Layout principal
        main_layout = QVBoxLayout(self)

        # --- Formulário para adicionar novo produto ---
        form_layout = QHBoxLayout()
        self.nome_input = QLineEdit()
        self.nome_input.setPlaceholderText("Nome do Produto")
        self.preco_input = QLineEdit()
        self.preco_input.setPlaceholderText("Preço (ex: 12.50)")
        self.add_button = QPushButton("Adicionar")

        form_layout.addWidget(QLabel("Nome:"))
        form_layout.addWidget(self.nome_input)
        form_layout.addWidget(QLabel("Preço:"))
        form_layout.addWidget(self.preco_input)
        form_layout.addWidget(self.add_button)
        main_layout.addLayout(form_layout)

        # --- Tabela para listar produtos ---
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Nome do Produto", "Preço (R$)"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers) # Trava a edição direta na tabela
        main_layout.addWidget(self.table)

        # --- Botão de fechar ---
        self.close_button = QPushButton("Fechar")
        main_layout.addWidget(self.close_button, alignment=Qt.AlignmentFlag.AlignRight)

        # --- Conectar Sinais e Slots (Eventos) ---
        self.add_button.clicked.connect(self.add_product)
        self.close_button.clicked.connect(self.accept) # 'accept' fecha o diálogo

        # Carrega os produtos existentes na tabela
        self.load_products()

    def load_products(self):
        """Carrega todos os produtos do banco e os exibe na tabela."""
        products = self.db_manager.get_all_products()
        self.table.setRowCount(len(products))

        for row, product in enumerate(products):
            self.table.setItem(row, 0, QTableWidgetItem(product.nome))
            self.table.setItem(row, 1, QTableWidgetItem(f"{product.preco:.2f}"))

    def add_product(self):
        """Pega os dados dos inputs e chama o gerenciador do banco para adicionar."""
        nome = self.nome_input.text().strip()
        preco_str = self.preco_input.text().strip().replace(',', '.')

        # Validação dos campos
        if not nome or not preco_str:
            QMessageBox.warning(self, "Erro", "Ambos os campos devem ser preenchidos.")
            return

        try:
            preco = float(preco_str)
            if preco <= 0:
                raise ValueError()
        except ValueError:
            QMessageBox.warning(self, "Erro", "O preço deve ser um número positivo.")
            return

        # Tenta adicionar no banco
        new_product = self.db_manager.add_product(nome, preco)

        if new_product:
            QMessageBox.information(self, "Sucesso", f"Produto '{nome}' adicionado com sucesso!")
            self.nome_input.clear()
            self.preco_input.clear()
            self.load_products() # Recarrega a tabela para mostrar o novo produto
        else:
            QMessageBox.warning(self, "Erro", f"Produto '{nome}' já existe no cadastro.")

    def closeEvent(self, event):
        """Garante que a sessão do banco seja fechada ao fechar a janela."""
        self.db_manager.close()
        super().closeEvent(event)