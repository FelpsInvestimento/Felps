# ia_venda.py

import time
from novadax_api import NovadaxAPI
from ia_analise import IAAnalise

class IAVenda:
    def __init__(self, api_key, api_secret):
        self.novadax = NovadaxAPI(api_key, api_secret)
        self.ia_analise = IAAnalise(api_key, api_secret)

    def executar_vendas(self, percentual_lucro_min=0.02):
        """
        Executa ordens de venda nos ativos comprados que atingiram o percentual mínimo de lucro.
        - percentual_lucro_min: lucro mínimo desejado (ex: 2% = 0.02)
        """
        ativos_comprados = self.novadax.get_open_positions()  # Posições abertas
        for ativo in ativos_comprados:
            preco_atual = self.novadax.get_market_price(ativo['ativo'])
            preco_medio = ativo['preco_medio']
            lucro = (preco_atual - preco_medio) / preco_medio

            if lucro >= percentual_lucro_min:
                ordem = self.novadax.create_order(
                    ativo['ativo'],
                    side="SELL",
                    quantidade=ativo['quantidade'],
                    preco=preco_atual
                )
                print(f"[IA VENDA] Ordem executada: {ativo['ativo']} | Quantidade: {ativo['quantidade']:.6f} | Preço: {preco_atual} | Lucro: {lucro*100:.2f}%")
            else:
                print(f"[IA VENDA] Não atingiu lucro mínimo: {ativo['ativo']} | Lucro atual: {lucro*100:.2f}%")

# Exemplo de uso
if __name__ == "__main__":
    import os
    ia_venda = IAVenda(api_key=os.getenv("NOVADEX_KEY"), api_secret=os.getenv("NOVADEX_SECRET"))
    while True:
        ia_venda.executar_vendas(percentual_lucro_min=0.02)
        time.sleep(15)  # Verifica vendas a cada 15 segundos
