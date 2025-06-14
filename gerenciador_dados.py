import json
import os

ARQUIVO_PRODUTOS = "produtos.json"
ARQUIVO_VENDAS = "vendas.json"

def verificar_arquivos():
    """Garante que os arquivos JSON existam."""
    if not os.path.exists(ARQUIVO_PRODUTOS):
        with open(ARQUIVO_PRODUTOS, 'w') as f:
            json.dump([], f)
    if not os.path.exists(ARQUIVO_VENDAS):
        with open(ARQUIVO_VENDAS, 'w') as f:
            json.dump([], f)

def carregar_dados(caminho_arquivo):
    """Carrega dados de um arquivo JSON."""
    verificar_arquivos()
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def salvar_dados(caminho_arquivo, dados):
    """Salva dados em um arquivo JSON."""
    verificar_arquivos()
    with open(caminho_arquivo, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)