# Configurações principais do Felps Trade

CONFIG = {
    # Lista de contas conectadas com suas chaves API (até 10 contas)
    'api_keys': [
        {
            'name': 'Conta 1',
            'access_key': 'fb17caa1-00a5-45ad-800f-31dcff935376',
            'secret_key': 'IDqP2LKyivmnBprsRQ8qzLt6oQPQNWGo'
        },
        {
            'name': 'Conta 2',
            'access_key': 'COLOQUE_SUA_ACCESS_KEY_AQUI',
            'secret_key': 'COLOQUE_SUA_SECRET_KEY_AQUI'
        },
        # Adicione até 10 contas seguindo o mesmo formato
    ],

    # Configuração inicial do stop inteligente (em %)
    'stop_percent': 2,  # Pode ser alterado pelo frontend

    # Modo de operação padrão
    # Valores possíveis: 'leve', 'moderado', 'agressivo', 'automático'
    'default_mode': 'automático',

    # Configurações gerais
    'backend_host': '0.0.0.0',
    'backend_port': 5000,
    'log_file': 'felps_trade.log'
}
