# ia_compra.py

import time
from novadax_api import NovadaxAPI
from ia_analise import IAAnalise

class IACompra:
    def __init__(self, api_key, api_secret):
        self.novadax = NovadaxAPI(api_key, api_secret)
        self.ia_analise = IAAnalise(api_key, api_secret)

    def executar_compras(self, top_n=3, percentual_compra=0.05):
        """
        Executa ordens de compra nos ativos mais promissores.
        - top_n: número de ativos a comprar
        - percentual_compra: porcentagem do saldo disponível para cada ativo
        """
        melhores_ativos = self.ia_analise.get_melhores_ativos(top_n=top_n)
        saldo_disponivel = self.novadax.get_balance("BRL")  # Pode alterar para USDT ou outra moeda base

        for ativo in melhores_ativos:
            valor_compra = saldo_disponivel * percentual_compra
            preco_atual = self.novadax.get_market_price(ativo['ativo'])
            quantidade = valor_compra / preco_atual

            if quantidade > 0:
                ordem = self.novadax.create_order(
                    ativo['ativo'],
                    side="BUY",
                    quantidade=quantidade,
                    preco=preco_atual
                )
                print(f"[IA COMPRA] Ordem executada: {ativo['ativo']} | Quantidade: {quantidade:.6f} | Preço: {preco_atual}")
            else:
                print(f"[IA COMPRA] Saldo insuficiente para comprar {ativo['ativo']}")

# Exemplo de uso
if __name__ == "__main__":
    import os
    ia_compra = IACompra(api_key=os.getenv("NOVADEX_KEY"), api_secret=os.getenv("NOVADEX_SECRET"))
    while True:
        ia_compra.executar_compras(top_n=3, percentual_compra=0.05)
        time.sleep(15)  # Executa compras a cada 15 segundos
