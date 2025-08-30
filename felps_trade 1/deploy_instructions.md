# Instruções de Deploy - FELPS TRADE

## Preparação para Deploy no Render

### 1. Estrutura do Projeto

O projeto FELPS TRADE está organizado da seguinte forma:

```
felps_trade/
├── backend/          # Aplicação Flask (API)
├── frontend/         # Aplicação React (Interface)
├── README.md         # Documentação do projeto
└── .gitignore        # Arquivos a serem ignorados pelo Git
```

### 2. Deploy do Backend (Flask)

**Arquivo necessário para o Render:**
- O backend já está configurado para rodar na porta 5000
- As dependências estão listadas em `backend/requirements.txt`
- As variáveis de ambiente devem ser configuradas no Render

**Configurações no Render:**
1. Conecte seu repositório GitHub
2. Selecione "Web Service"
3. Configure:
   - **Build Command:** `cd backend && pip install -r requirements.txt`
   - **Start Command:** `cd backend && PYTHONPATH=/opt/render/project/src/backend python app/main.py`
   - **Environment:** Python 3
   - **Root Directory:** deixe em branco (raiz do projeto)

**Variáveis de Ambiente no Render:**
```
NOVADAX_ACCESS_KEY=fb17caa1-00a5-45ad-800f-31dcff935376
NOVADAX_SECRET_KEY=IDqP2LKyivmnBprsRQ8qzLt6oQPQNWGo
```

### 3. Deploy do Frontend (React)

**Preparação:**
1. Atualize a URL da API no frontend para apontar para o backend deployado
2. Faça o build da aplicação React

**Configurações no Render:**
1. Selecione "Static Site"
2. Configure:
   - **Build Command:** `cd frontend && npm install && npm run build`
   - **Publish Directory:** `frontend/dist`
   - **Root Directory:** deixe em branco (raiz do projeto)

### 4. Configuração de CORS

O backend já está configurado com Flask-CORS para aceitar requisições de qualquer origem.

### 5. Monitoramento

Após o deploy:
- Verifique os logs do backend no Render
- Teste todas as funcionalidades da interface
- Monitore o desempenho das IAs

## Observações Importantes

1. **Segurança das Chaves de API:** As chaves da NovaDAX devem ser configuradas como variáveis de ambiente no Render, nunca no código.

2. **Limitações da API:** A API da NovaDAX tem limites de taxa (6000 peso por minuto). O robô está configurado para respeitar esses limites.

3. **Operação 24/7:** O Render mantém os serviços ativos 24/7, permitindo que o robô opere continuamente.

4. **Logs e Monitoramento:** Use os logs do Render para monitorar o comportamento do robô e identificar possíveis problemas.

## URLs Após Deploy

- **Backend:** `https://seu-backend.onrender.com`
- **Frontend:** `https://seu-frontend.onrender.com`

Lembre-se de atualizar a URL da API no frontend após o deploy do backend.

