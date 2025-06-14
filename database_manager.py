from database import setup_database, Produto

class DatabaseManager:
    def __init__(self):
        """Inicializa o gerenciador e estabelece a sessão com o banco."""
        self.session = setup_database()

    def add_product(self, nome, preco):
        """Adiciona um novo produto ao banco de dados."""
        # Validação simples para evitar produtos duplicados
        produto_existente = self.session.query(Produto).filter_by(nome=nome).first()
        if produto_existente:
            print(f"Produto '{nome}' já existe.")
            return None # Retorna None para indicar que não foi adicionado
            
        novo_produto = Produto(nome=nome, preco=preco)
        self.session.add(novo_produto)
        self.session.commit()
        print(f"Produto '{nome}' adicionado com sucesso.")
        return novo_produto

    def get_all_products(self):
        """Retorna uma lista de todos os produtos cadastrados."""
        return self.session.query(Produto).order_by(Produto.nome).all()

    def close(self):
        """Fecha a sessão do banco de dados."""
        self.session.close()