# Sistema de Comanda Eletrônica

![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)

Um sistema de Ponto de Venda (PDV) simples, desenvolvido em Python com uma interface gráfica moderna e intuitiva inspirada em comandas de restaurante. O projeto utiliza CustomTkinter para a interface e JSON para o armazenamento de dados.

## Screenshots

*(Dica: Tire screenshots do seu programa em execução e substitua os links abaixo. Isso deixa o README muito mais atrativo!)*

![Tela Principal](https://i.imgur.com/your_main_screen_image_link.png "Tela Principal da Comanda")
*Tela principal de registro de vendas.*

![Tela de Gerenciamento](https://i.imgur.com/your_products_screen_image_link.png "Tela de Gerenciamento de Produtos")
*Tela para adicionar e excluir produtos.*

## Funcionalidades

-   :heavy_plus_sign: **Gerenciamento de Produtos:** Adicione e exclua produtos com nome e preço de forma fácil e rápida.
-   :scroll: **Registro de Vendas:** Crie "comandas" adicionando múltiplos produtos e quantidades.
-   :moneybag: **Cálculo de Total:** O valor total da comanda é calculado e exibido em tempo real.
-   :floppy_disk: **Persistência de Dados:** Todos os produtos e vendas finalizadas são salvos em arquivos JSON, permitindo que os dados persistam entre as execuções do programa.
-   :art: **Interface Gráfica Moderna:** Construído com a biblioteca CustomTkinter, oferecendo um visual agradável e responsivo.

## Tecnologias Utilizadas

-   **Python 3**
-   **CustomTkinter** - Para a criação da interface gráfica.
-   **JSON** - Para armazenamento leve e legível dos dados de produtos e vendas.

## Instalação e Execução

Siga os passos abaixo para executar o projeto em sua máquina local.

**1. Clone o Repositório**
```bash
git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/19lemabe94/GestorVendas.git)
cd seu-repositorio
```

**2. Crie e Ative o Ambiente Virtual**

Um ambiente virtual é essencial para isolar as dependências do projeto.

-   **Windows (PowerShell):**
    ```powershell
    # Criar o ambiente
    python -m venv venv
    # Ativar o ambiente
    .\venv\Scripts\Activate.ps1
    ```

-   **Linux / macOS:**
    ```bash
    # Criar o ambiente
    python3 -m venv venv
    # Ativar o ambiente
    source venv/bin/activate
    ```
    Você saberá que o ambiente está ativo quando vir `(venv)` no início do seu prompt de comando.

**3. Instale as Dependências**

O arquivo `requirements.txt` contém todas as bibliotecas Python necessárias.
```bash
pip install -r requirements.txt
```

**4. Execute a Aplicação**

Com o ambiente virtual ainda ativo, inicie o programa:
```bash
python main.py
```

## Estrutura do Projeto
```
/GestorVendas/
|-- .gitignore
|-- main.py                 # Ponto de entrada da aplicação (Tela da Comanda)
|-- tela_produtos.py        # Módulo da tela de gerenciamento de produtos
|-- gerenciador_dados.py    # Funções para ler e salvar os arquivos JSON
|-- produtos.json           # Banco de dados de produtos
|-- vendas.json             # Histórico de todas as vendas
|-- requirements.txt        # Lista de dependências do projeto
|-- README.md               # Este arquivo
|-- venv/                     # Pasta do ambiente virtual (ignorada pelo Git)
```

## Próximos Passos e Melhorias

O projeto pode ser expandido com as seguintes funcionalidades:

-   [ ] Implementar a função de **Editar** um produto existente.
-   [ ] Criar uma tela para **visualizar o histórico de vendas**.
-   [ ] Adicionar funcionalidades de **busca e filtro** na tela de produtos.
-   [ ] Gerar um **relatório de análise** (ex: produto mais vendido, faturamento diário).
-   [ ] Criar um executável (`.exe` ou similar) com PyInstaller para facilitar a distribuição.


## ✨ Autor
Leonardo Bezerra:

[GITHUB](https://github.com/19lemabe94) | [LinkedIn](https://www.linkedin.com/in/leonardo-bezerra-98b05a307/)