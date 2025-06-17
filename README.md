# Sistema de Comanda Eletrônica

![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)

Um sistema de Ponto de Venda (PDV) completo, desenvolvido em Python com uma interface gráfica moderna e intuitiva inspirada em comandas de restaurante. O projeto agora conta com gerenciamento de produtos por categoria, relatórios avançados com filtros dinâmicos e gerenciamento do histórico de vendas.

## Screenshots

*(Dica: Tire screenshots do seu programa em execução e substitua os links abaixo para mostrar todo o potencial do seu sistema!)*

| Tela Principal | Gerenciamento de Produtos |
| :---: | :---: |
| ![Tela Principal](https://i.imgur.com/your_main_screen_image_link.png "Tela Principal da Comanda") | ![Tela de Gerenciamento](https://i.imgur.com/your_products_screen_image_link.png "Tela de Gerenciamento de Produtos") |

| Relatórios Avançados | Histórico de Vendas |
| :---: | :---: |
| ![Tela de Relatórios](https://i.imgur.com/your_reports_screen_image_link.png "Tela de Relatórios com Filtros") | ![Tela de Histórico](https://i.imgur.com/your_history_screen_image_link.png "Tela de Histórico de Vendas") |

## Funcionalidades Principais

-   :heavy_plus_sign: **Gerenciamento de Produtos:** Adicione, exclua e categorize produtos (Lanches, Bebidas, etc.) em uma interface dedicada.
-   :scroll: **Registro de Vendas Flexível:** Crie "comandas" adicionando múltiplos produtos e cancele/limpe o pedido a qualquer momento com um único botão.
-   :chart_with_upwards_trend: **Relatórios Avançados:** Analise o desempenho das vendas com uma tela de relatórios que permite:
    -   Filtrar vendas por **período de datas**.
    -   Filtrar vendas por uma ou mais **categorias**.
    -   Visualizar o faturamento **hora a hora** para identificar horários de pico.
-   :wastebasket: **Gerenciamento de Histórico:** Visualize todas as vendas já realizadas em uma lista e exclua registros específicos de forma segura, com confirmação.
-   :floppy_disk: **Persistência de Dados:** Todos os produtos e vendas finalizadas são salvos em arquivos JSON, permitindo que os dados persistam entre as execuções.
-   :art: **Interface Gráfica Moderna:** Construído com a biblioteca CustomTkinter, oferecendo um visual agradável e responsivo em tema claro ou escuro.

## Tecnologias Utilizadas

-   **Python 3**
-   **CustomTkinter** - Para a criação da interface gráfica.
-   **tkcalendar** - Para os widgets de seleção de data nos filtros.
-   **JSON** - Para armazenamento leve e legível dos dados de produtos e vendas.

## Instalação e Execução

Siga os passos abaixo para executar o projeto em sua máquina local.

**1. Clone o Repositório**
```bash
git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
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
|-- gerenciador_dados.py    # Funções para ler e salvar os arquivos JSON
|-- main.py                 # Ponto de entrada da aplicação (Tela da Comanda)
|-- tela_historico_vendas.py# Módulo da tela de gerenciamento do histórico
|-- tela_produtos.py        # Módulo da tela de gerenciamento de produtos
|-- tela_relatorios.py      # Módulo da tela de relatórios avançados
|-- produtos.json           # Banco de dados de produtos
|-- vendas.json             # Histórico de todas as vendas
|-- requirements.txt        # Lista de dependências do projeto
|-- README.md               # Este arquivo
|-- venv/                     # Pasta do ambiente virtual (ignorada pelo Git)
```

## Próximos Passos e Melhorias

O projeto pode ser expandido com as seguintes funcionalidades:

-   [ ] Implementar a função de **Editar** um produto existente.
-   [ ] Adicionar **gráficos** à tela de relatórios (usando Matplotlib).
-   [ ] Implementar "soft delete" (marcar uma venda como "cancelada" em vez de excluir).
-   [ ] Adicionar busca e filtro na tela de gerenciamento de produtos.
-   [ ] Criar um sistema de **backup e restauração** dos arquivos JSON.
-   [ ] Desenvolver um sistema de autenticação de usuários (login/senha).
-   [ ] Criar um executável (`.exe` ou similar) com PyInstaller para facilitar a distribuição.

## ✨ Autor
Leonardo Bezerra:

[GITHUB](https://github.com/19lemabe94) | [LinkedIn](https://www.linkedin.com/in/leonardo-bezerra-98b05a307/)