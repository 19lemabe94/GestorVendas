# Sistema de Comanda Eletrônica

![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)

Um sistema de Ponto de Venda (PDV) completo, desenvolvido em Python com uma interface gráfica moderna e intuitiva inspirada em comandas de restaurante. O projeto conta com gerenciamento de produtos por categoria, relatórios avançados com filtros dinâmicos e gerenciamento do histórico de vendas.

## Screenshots

| Tela Principal | Gerenciamento de Produtos |
| :---: | :---: |
| ![Tela Principal](https://raw.githubusercontent.com/19lemabe94/GestorVendas/main/prints/tela1.png "Tela Principal da Comanda") | ![Tela de Gerenciamento](https://raw.githubusercontent.com/19lemabe94/GestorVendas/main/prints/tela2.png "Tela de Gerenciamento de Produtos") |

| Relatórios Avançados | Histórico de Vendas |
| :---: | :---: |
| ![Tela de Relatórios](https://raw.githubusercontent.com/19lemabe94/GestorVendas/main/prints/tela3.png "Tela de Relatórios com Filtros") | ![Tela de Histórico](https://raw.githubusercontent.com/19lemabe94/GestorVendas/main/prints/tela4.png "Tela de Histórico de Vendas") |


## Funcionalidades Principais

-   :heavy_plus_sign: **Gerenciamento de Produtos:** Adicione, edite, exclua e categorize produtos (Lanches, Bebidas, etc.) em uma interface com busca e filtro.
-   :scroll: **Registro de Vendas Flexível:** Crie "comandas" adicionando múltiplos produtos e cancele/limpe o pedido a qualquer momento com um único botão.
-   :chart_with_upwards_trend: **Relatórios Avançados:** Analise o desempenho das vendas com uma tela de relatórios que permite:
    -   Filtrar vendas por **período de datas**.
    -   Filtrar vendas por uma ou mais **categorias**.
    -   Visualizar o faturamento **hora a hora** para identificar horários de pico.
-   :wastebasket: **Gerenciamento de Histórico:** Visualize todas as vendas já realizadas em uma lista e exclua registros específicos de forma segura, com confirmação.
-   :floppy_disk: **Persistência de Dados:** Todos os produtos e vendas finalizadas são salvos em arquivos JSON.
-   :art: **Interface Gráfica Moderna:** Construído com a biblioteca CustomTkinter.

## Tecnologias Utilizadas

-   **Python 3**
-   **CustomTkinter** - Para a criação da interface gráfica.
-   **tkcalendar** - Para os widgets de seleção de data nos filtros.
-   **JSON** - Para armazenamento leve e legível dos dados.

## Instalação e Execução

Siga os passos abaixo para executar o projeto em sua máquina local.

**1. Clone o Repositório**
```bash
git clone [https://github.com/19lemabe94/GestorVendas.git](https://github.com/19lemabe94/GestorVendas.git)
cd GestorVendas
```

**2. Crie e Ative o Ambiente Virtual**

-   **Windows (PowerShell):**
    ```powershell
    python -m venv venv
    .\venv\Scripts\Activate.ps1
    ```

-   **Linux / macOS:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

**3. Instale as Dependências**
```bash
pip install -r requirements.txt
```

**4. Execute a Aplicação**
```bash
python main.py
```

## Estrutura do Projeto
```
/GestorVendas/
|-- prints/                 # Pasta com as imagens do projeto
|   |-- tela1.png
|   |-- tela2.png
|   |-- tela3.png
|   |-- tela4.png
|-- .gitignore
|-- gerenciador_dados.py
|-- main.py
|-- tela_historico_vendas.py
|-- tela_produtos.py
|-- tela_relatorios.py
|-- produtos.json
|-- vendas.json
|-- requirements.txt
|-- README.md
|-- venv/
```

## Próximos Passos e Melhorias

-   [ ] Adicionar **gráficos** à tela de relatórios (usando Matplotlib).
-   [ ] Implementar "soft delete" (marcar uma venda como "cancelada" em vez de excluir).
-   [ ] Criar um sistema de **backup e restauração** dos arquivos JSON.
-   [ ] Desenvolver um sistema de autenticação de usuários (login/senha).
-   [ ] Criar um executável (`.exe`) com PyInstaller para facilitar a distribuição.

## Autor

**Leonardo Bezerra**

[GITHUB](https://github.com/19lemabe94) | [LinkedIn](https://www.linkedin.com/in/leonardo-bezerra-98b05a307/)