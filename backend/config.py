# backend/config.py

# ================================
# CONFIGURAÇÕES DE CONTAS (API KEYS)
# ================================
# ⚠️ IMPORTANTE: coloque aqui suas chaves da NovaDAX
# Cada conta terá uma API_KEY e SECRET_KEY própria

CONTAS = {
    "conta1": {
        "API_KEY": "SUA_API_KEY_AQUI",
        "SECRET_KEY": "SEU_SECRET_KEY_AQUI"
    },
    "conta2": {
        "API_KEY": "SUA_API_KEY_AQUI",
        "SECRET_KEY": "SEU_SECRET_KEY_AQUI"
    },
    "conta3": {
        "API_KEY": "SUA_API_KEY_AQUI",
        "SECRET_KEY": "SEU_SECRET_KEY_AQUI"
    },
    # ...
    # até conta10
}

# ================================
# CONFIGURAÇÕES DE OPERAÇÃO
# ================================

# Stop Loss inteligente (percentual)
STOP_LOSS_PERCENT = 0.02  # 2% (ajustável entre 0.01 e 0.02)

# Modos de operação
MODOS = {
    "leve": {
        "risco": "baixo",
        "alocacao": 0.05  # 5% do saldo em cada operação
    },
    "moderado": {
        "risco": "médio",
        "alocacao": 0.15  # 15% do saldo em cada operação
    },
    "agressivo": {
        "risco": "alto",
        "alocacao": 0.30  # 30% do saldo em cada operação
    },
    "automatico": {
        "risco": "dinâmico",
        "alocacao": None  # AI decide
    }
}

# ================================
# CONFIGURAÇÕES GERAIS
# ================================

# Quantidade máxima de ativos diferentes monitorados por vez
MAX_ATIVOS = 20

# Intervalo de análise de mercado (em segundos)
INTERVALO_ANALISE = 15

# Nome oficial do robô
ROBO_NOME = "FELPS TRADE"

# Mensagem de motivação
MOTIVACAO = "EU QUERO, EU POSSO E EU CONSIGO. JÁ DEU CERTO."
