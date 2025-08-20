# ia_stoploss.py

import time
from novadax_api import NovadaxAPI

class IAStopLoss:
    def __init__(self, api_key, api_secret, percentual_stop=0.02):
        """
        - percentual_stop: define o stop loss máximo permitido (ex: 0.02 = 2%)
        """
        self.novadax = NovadaxAPI(api_key, api_secret)
        self.percentual_stop = percentual_stop

    def verificar_stoploss(self):
        """
        Verifica todas as posições abertas e executa venda automática se o prejuízo
        ultrapassar o percentual definido.
        """
        ativos_comprados = self.novadax.get_open_positions()
        for ativo in ativos_comprados:
            preco_atual = self.novadax.get_market_price(ativo['ativo'])
            preco_medio = ativo['preco_medio']
            perda = (preco_medio - preco_atual) / preco_medio

            if perda >= self.percentual_stop:
                ordem = self.novadax.create_order(
                    ativo['ativo'],
                    side="SELL",
                    quantidade=ativo['quantidade'],
                    preco=preco_atual
                )
                print(f"[STOP LOSS] Vendido {ativo['ativo']} | Quantidade: {ativo['quantidade']:.6f} | Preço: {preco_atual} | Perda: {perda*100:.2f}%")
            else:
                print(f"[STOP LOSS] Seguro: {ativo['ativo']} | Perda atual: {perda*100:.2f}%")

# Exemplo de uso
if __name__ == "__main__":
    import os
    ia_stoploss = IAStopLoss(api_key=os.getenv("NOVADEX_KEY"), api_secret=os.getenv("NOVADEX_SECRET"), percentual_stop=0.02)
    while True:
        ia_stoploss.verificar_stoploss()
        time.sleep(10)  # Verifica stop loss a cada 10 segundos
