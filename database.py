import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from datetime import datetime

# Define a base para nossos modelos
Base = declarative_base()

# Modelo: Tabela de Produtos
class Produto(Base):
    __tablename__ = 'produtos'
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False, unique=True)
    preco = Column(Float, nullable=False)

# Modelo: Tabela de Comandas
class Comanda(Base):
    __tablename__ = 'comandas'
    id = Column(Integer, primary_key=True)
    data_criacao = Column(DateTime, default=datetime.now)
    status = Column(String(20), default='aberta') # aberta, fechada
    total = Column(Float, default=0.0)
    # Relação com os itens da comanda
    itens = relationship("ItemComanda", back_populates="comanda", cascade="all, delete-orphan")

# Modelo: Tabela de Itens dentro de uma Comanda
class ItemComanda(Base):
    __tablename__ = 'itens_comanda'
    id = Column(Integer, primary_key=True)
    comanda_id = Column(Integer, ForeignKey('comandas.id'))
    produto_id = Column(Integer, ForeignKey('produtos.id'))
    quantidade = Column(Integer, nullable=False)
    preco_unitario = Column(Float, nullable=False)

    # Relações
    comanda = relationship("Comanda", back_populates="itens")
    produto = relationship("Produto")

# Função para configurar e retornar a engine e a sessão do banco de dados
def setup_database():
    # Cria a engine do banco de dados. O arquivo 'vendas.db' será criado na pasta.
    engine = create_engine('sqlite:///vendas.db')
    # Cria as tabelas no banco de dados, se elas não existirem
    Base.metadata.create_all(engine)
    # Cria uma fábrica de sessões para interagir com o banco de dados
    Session = sessionmaker(bind=engine)
    return Session()

# Para testar, podemos executar este arquivo diretamente
if __name__ == '__main__':
    session = setup_database()
    print("Banco de dados 'vendas.db' e tabelas criadas com sucesso!")
    # Exemplo de como adicionar um produto
    # novo_produto = Produto(nome='Café Expresso', preco=5.0)
    # session.add(novo_produto)
    # session.commit()
    # print("Produto de exemplo adicionado.")