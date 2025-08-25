# FELPS TRADE

## Robô de Day Trade 100% Automático com IAs

"EU QUERO, EU POSSO E EU CONSIGO. JÁ DEU CERTO."

Este projeto visa desenvolver um robô de day trade totalmente automatizado, o "FELPS TRADE", utilizando inteligência artificial para análise, compra, venda, stop loss inteligente e supervisão. O robô será integrado à corretora NovaDAX via API, permitindo operações 24 horas por dia em múltiplos ativos financeiros, como criptomoedas, memecoins, altcoins, tokens, stablecoins, Ouro, Euro, Dólar, Ações nacionais e internacionais, NFTs, e outros ativos explosivos.

## Funcionalidades Principais

-   **5 IAs Integradas:**
    -   IA de Análise
    -   IA de Compra
    -   IA de Venda
    -   IA de Stop Loss Inteligente (com 1% a 2% de stop de saída)
    -   IA Supervisora
-   **Integração com NovaDAX:** Conexão via API para operações e consulta de saldo em tempo real.
-   **Operações Múltiplas e Simultâneas:** Capacidade de operar em diversos ativos financeiros simultaneamente.
-   **Operação 24/7:** Projetado para rodar continuamente em ambiente de nuvem.
-   **Interface Simples:**
    -   Relatório em texto das operações.
    -   Opções de modo: Leve, Moderado, Agressivo e Automático (determinado pelas IAs).
    -   Visualização do saldo disponível na corretora em tempo real.
    -   Confirmação de funcionamento das IAs.
-   **Gestão de Múltiplas Contas:** Suporte para até 10 contas separadas com APIs diferentes, operando de forma igual e simultânea, com exibição do saldo de cada uma separadamente.

## Estrutura do Projeto

O projeto é dividido em duas partes principais: **Backend** (lógica de negócio e IAs) e **Frontend** (interface do usuário).

```
felps_trade/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── routes.py
│   │   ├── models.py
│   │   ├── services/
│   │   │   ├── novadax_api.py
│   │   │   └── trade_manager.py
│   │   ├── ias/
│   │   │   ├── analysis_ia.py
│   │   │   ├── buy_ia.py
│   │   │   ├── sell_ia.py
│   │   │   ├── stop_loss_ia.py
│   │   │   └── supervisor_ia.py
│   │   └── utils/
│   │       └── config.py
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── App.js
│   │   ├── index.js
│   │   ├── components/
│   │   │   ├── Header.js
│   │   │   ├── Dashboard.js
│   │   │   └── ReportTable.js
│   │   ├── styles/
│   │   │   └── App.css
│   │   └── api/
│   │       └── felps_trade_api.js
│   ├── package.json
│   └── .env
├── .gitignore
└── README.md
```

## Tecnologias Utilizadas

-   **Backend:** Python, Flask, `python-dotenv`, `requests` (para API NovaDAX), bibliotecas de ML (ex: `scikit-learn`, `pandas`, `numpy`).
-   **Frontend:** JavaScript, React.

## Configuração e Execução (Local)

### Backend

1.  Navegue até `felps_trade/backend`.
2.  Crie um arquivo `.env` com suas chaves da NovaDAX:
    ```
    NOVADAX_ACCESS_KEY=sua_access_key
    NOVADAX_SECRET_KEY=sua_secret_key
    ```
3.  Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```
4.  Execute a aplicação Flask:
    ```bash
    python app/main.py
    ```

### Frontend

1.  Navegue até `felps_trade/frontend`.
2.  Crie um arquivo `.env` com a URL do seu backend (se estiver rodando localmente, será algo como `REACT_APP_BACKEND_URL=http://localhost:5000`).
3.  Instale as dependências:
    ```bash
    npm install
    # ou yarn install
    ```
4.  Inicie a aplicação React:
    ```bash
    npm start
    # ou yarn start
    ```

## Deploy no Render

O projeto será configurado para deploy contínuo no Render, com o backend como um Web Service e o frontend como um Static Site. As variáveis de ambiente com as chaves da NovaDAX serão configuradas diretamente no Render para segurança.

## Contribuição

Sinta-se à vontade para contribuir com o projeto. Para isso, siga as diretrizes de contribuição e o código de conduta.

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

