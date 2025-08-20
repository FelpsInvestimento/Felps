# ia_analise.py

import time
from novadax_api import NovadaxAPI
from utils import calcular_indicadores

class IAAnalise:
    def __init__(self, api_key, api_secret):
        self.novadax = NovadaxAPI(api_key, api_secret)
        self.ativos_info = {}

    def analisar_ativos(self):
        """
        Analisa todos os ativos disponíveis na corretora e calcula indicadores importantes
        para decidir se devem ser monitorados para compra ou venda.
        """
        ativos = self.novadax.get_all_assets()
        resultados = []

        for ativo in ativos:
            dados = self.novadax.get_market_data(ativo)
            indicadores = calcular_indicadores(dados)
            score = indicadores['momentum'] + indicadores['volume'] * 0.5 - indicadores['risco'] * 0.3

            resultado = {
                "ativo": ativo,
                "score": score,
                "indicadores": indicadores,
                "timestamp": time.time()
            }

            resultados.append(resultado)

        self.ativos_info = {r['ativo']: r for r in resultados}
        return resultados

    def get_melhores_ativos(self, top_n=5):
        """
        Retorna os top_n ativos com maior score de análise.
        """
        if not self.ativos_info:
            self.analisar_ativos()
        sorted_ativos = sorted(self.ativos_info.values(), key=lambda x: x['score'], reverse=True)
        return sorted_ativos[:top_n]

# Exemplo de uso
if __name__ == "__main__":
    import os
    ia = IAAnalise(api_key=os.getenv("NOVADEX_KEY"), api_secret=os.getenv("NOVADEX_SECRET"))
    while True:
        melhores = ia.get_melhores_ativos()
        print("Top ativos analisados:")
        for ativo in melhores:
            print(f"{ativo['ativo']} - Score: {ativo['score']:.2f}")
        time.sleep(10)  # Analisa a cada 10 segundos
