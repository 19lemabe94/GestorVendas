# Sistema de Comanda Eletrônica (Gestor de Vendas)

![Status](https://img.shields.io/badge/status-Pronto%20para%20Uso-brightgreen)

Um sistema de Ponto de Venda (PDV) completo e funcional, desenvolvido em Python com a biblioteca CustomTkinter. Inspirado em comandas de restaurante, este projeto oferece uma solução robusta para gerenciamento de produtos, registro de vendas e análise de dados, empacotado em um executável para fácil distribuição.

## Como Usar (Para Usuários Finais)

Você pode usar o programa sem precisar instalar Python ou qualquer dependência.

1.  Acesse a página de **[Releases](https://github.com/19lemabe94/GestorVendas/releases)** do projeto.
2.  Na versão mais recente, baixe o arquivo `.zip` (ex: `GestorVendas_v1.0.0.zip`).
3.  Extraia o conteúdo do arquivo `.zip` em uma pasta no seu computador.
4.  Execute o arquivo `main.exe`. Pronto!

---
> ### :warning: AVISO IMPORTANTE SOBRE ANTIVÍRUS (FALSO POSITIVO)
>
> **O programa é 100% seguro.** No entanto, alguns antivírus (especialmente o Windows Defender) podem identificar o arquivo `.exe` como uma ameaça (`Trojan:Win32/Bearfoos.B!ml` ou similar).
>
> **Por que isso acontece?** O PyInstaller, ferramenta usada para criar o `.exe`, empacota o código de uma forma que, para o antivírus, se parece com o comportamento de alguns malwares (um arquivo que se auto-extrai para rodar). Trata-se de um **falso positivo** muito comum para aplicações feitas por desenvolvedores independentes.
>
> **Como resolver:** Se o Windows bloquear o arquivo, vá em "Segurança do Windows" > "Proteção contra vírus e ameaças" > "Histórico de proteção". Encontre o item bloqueado, clique em "Ações" e selecione "Restaurar" ou "Permitir".
---

## Screenshots

| Tela Principal | Gerenciamento de Produtos |
| :---: | :---: |
| ![Tela Principal](https://raw.githubusercontent.com/19lemabe94/GestorVendas/main/prints/tela1.png "Tela Principal da Comanda") | ![Tela de Gerenciamento](https://raw.githubusercontent.com/19lemabe94/GestorVendas/main/prints/tela2.png "Tela de Gerenciamento de Produtos") |

| Relatórios Avançados | Histórico de Vendas |
| :---: | :---: |
| ![Tela de Relatórios](https://raw.githubusercontent.com/19lemabe94/GestorVendas/main/prints/tela3.png "Tela de Relatórios com Filtros") | ![Tela de Histórico](https://raw.githubusercontent.com/19lemabe94/GestorVendas/main/prints/tela4.png "Tela de Histórico de Vendas") |

## Funcionalidades Principais

-   :heavy_plus_sign: **Gerenciamento de Produtos:** CRUD completo (Adicionar, Editar, Excluir) com categorização, busca por nome e filtro por categoria.
-   :scroll: **Registro de Vendas Flexível:** Crie comandas, adicione itens e limpe o pedido a qualquer momento.
-   :credit_card: **Seleção de Pagamento:** Finalização de venda com seleção obrigatória de método (Dinheiro ou Cartão).
-   :chart_with_upwards_trend: **Relatórios Avançados:** Painel de análise com:
    -   Filtros dinâmicos por período de datas e categorias.
    -   Análise de faturamento hora a hora.
    -   Resumo rápido das vendas do dia, detalhado por método de pagamento.
-   :wastebasket: **Gerenciamento de Histórico:** Visualize e exclua vendas passadas de forma segura.
-   :floppy_disk: **Persistência de Dados:** Todos os dados são salvos localmente em arquivos JSON.

## Para Desenvolvedores: Rodando a Partir do Código-Fonte

Se você deseja executar o projeto a partir do código ou contribuir, siga os passos abaixo.

**1. Clone o Repositório**
```bash
git clone [https://github.com/19lemabe94/GestorVendas.git](https://github.com/19lemabe94/GestorVendas.git)
cd GestorVendas
```

**2. Crie e Ative o Ambiente Virtual**
```powershell
# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**3. Instale as Dependências**
```bash
pip install -r requirements.txt
```

**4. Execute a Aplicação**
```bash
python main.py
```

### Gerando o Executável (.exe)

Para empacotar a aplicação, certifique-se de que o `pyinstaller` está instalado (`pip install pyinstaller`) e execute o comando abaixo no terminal, a partir da raiz do projeto:

```bash
pyinstaller --noconsole --onefile --windowed --add-data="produtos.json;." --add-data="vendas.json;." --add-data="venv\Lib\site-packages\customtkinter;customtkinter" --add-data="venv\Lib\site-packages\tkcalendar;tkcalendar" main.py
```
O executável final estará na pasta `dist/`.

## Tecnologias Utilizadas

-   **Python 3**
-   **CustomTkinter**
-   **tkcalendar**
-   **JSON**
-   **PyInstaller** (para a distribuição)

## Próximos Passos e Melhorias

-   [ ] Adicionar **gráficos** à tela de relatórios (usando Matplotlib).
-   [ ] Implementar "soft delete" (marcar uma venda como "cancelada" em vez de excluir).
-   [ ] Criar um sistema de **backup e restauração** dos arquivos JSON.
-   [ ] Desenvolver um sistema de autenticação de usuários (login/senha).

## Autor

**Leonardo Bezerra**

[GITHUB](https://github.com/19lemabe94) | [LinkedIn](https://www.linkedin.com/in/leonardo-bezerra-98b05a307/)