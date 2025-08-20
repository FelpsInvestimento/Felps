# ia_supervisora.py

import time
from ia_analise import IAAnalise
from ia_compra import IACompra
from ia_venda import IAVenda
from ia_stoploss import IAStopLoss

class IASupervisora:
    def __init__(self, api_key, api_secret):
        self.ia_analise = IAAnalise(api_key, api_secret)
        self.ia_compra = IACompra(api_key, api_secret)
        self.ia_venda = IAVenda(api_key, api_secret)
        self.ia_stoploss = IAStopLoss(api_key, api_secret, percentual_stop=0.02)

    def executar_ciclo(self):
        """
        Ciclo principal do robô:
        1. Analisa ativos
        2. Executa compras nos melhores ativos
        3. Executa vendas em ativos com lucro
        4. Aplica stop loss inteligente
        """
        print("[SUPERVISORA] Iniciando ciclo de operação...")
        melhores_ativos = self.ia_analise.get_melhores_ativos()
        print(f"[SUPERVISORA] Top ativos: {[a['ativo'] for a in melhores_ativos]}")

        # Compra ativos promissores
        self.ia_compra.executar_compras(top_n=3, percentual_compra=0.05)

        # Vende ativos com lucro
        self.ia_venda.executar_vendas(percentual_lucro_min=0.02)

        # Aplica stop loss
        self.ia_stoploss.verificar_stoploss()

        print("[SUPERVISORA] Ciclo finalizado.\n")

# Exemplo de uso
if __name__ == "__main__":
    import os
    supervisora = IASupervisora(api_key=os.getenv("NOVADEX_KEY"), api_secret=os.getenv("NOVADEX_SECRET"))

    while True:
        supervisora.executar_ciclo()
        time.sleep(15)  # Executa o ciclo a cada 15 segundos
