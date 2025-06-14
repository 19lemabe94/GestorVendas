# main.py (versão atualizada)

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton

# Importe a nova janela que criamos
from product_dialog import ProductDialog 

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Gestor de Vendas")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.titulo_label = QLabel("Bem-vindo ao Gestor de Vendas")
        font = self.titulo_label.font()
        font.setPointSize(24)
        self.titulo_label.setFont(font)

        self.btn_nova_comanda = QPushButton("Nova Comanda")
        self.btn_ver_comandas = QPushButton("Visualizar Comandas")
        self.btn_cadastrar_produto = QPushButton("Cadastrar Produto")
        self.btn_analise = QPushButton("Análise de Vendas")

        layout.addWidget(self.titulo_label)
        layout.addWidget(self.btn_nova_comanda)
        layout.addWidget(self.btn_ver_comandas)
        layout.addWidget(self.btn_cadastrar_produto)
        layout.addWidget(self.btn_analise)

        # --- Conectar o botão para abrir a janela de produtos ---
        self.btn_cadastrar_produto.clicked.connect(self.open_product_dialog)

    def open_product_dialog(self):
        """Cria e exibe a janela de gerenciamento de produtos."""
        dialog = ProductDialog(self) # 'self' torna a janela principal a "mãe" do diálogo
        dialog.exec() # 'exec()' abre o diálogo de forma modal (bloqueia a janela principal)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())