import time
from utils.data_processing import DataProcessing
from utils.logger import Logger

class IndicatorIA:
    def __init__(self, analysis_ia, news_ia, interval=10):
        """
        Inicializa a IA de indicadores.
        analysis_ia: referência à IA de análise de ativos
        news_ia: referência à IA de notícias
        interval: tempo em segundos entre cálculos
        """
        self.analysis_ia = analysis_ia
        self.news_ia = news_ia
        self.dp = DataProcessing()
        self.logger = Logger()
        self.interval = interval
        self.status = "Iniciando"
        self.indicators = {}  # Ex: { "BTC": {"confidence": 80, "action": "BUY"} }

    def start(self):
        """
        Inicia o loop contínuo de cálculo de indicadores.
        """
        self.logger.log("IndicatorIA iniciada")
        self.status = "Rodando"
        while True:
            try:
                self.run_indicators()
            except Exception as e:
                self.logger.log(f"ERRO IndicatorIA: {e}")
            time.sleep(self.interval)

    def run_indicators(self):
        """
        Calcula os indicadores de confiança para cada ativo analisado.
        """
        best_assets = self.analysis_ia.best_assets
        for asset in best_assets:
            # Exemplo de cálculo simplificado
            confidence = 50  # base neutra
            sentiment = self.news_ia.get_sentiment(asset)
            if sentiment == "positivo":
                confidence += 30
            elif sentiment == "negativo":
                confidence -= 30

            # Pode adicionar aqui cálculo de médias móveis, volatilidade, volume, etc.
            df_asset = self.dp.process_market_data([{"symbol": asset, "price": 1, "volume": 1}])  # Exemplo placeholder
            # (Substituir com dados reais se disponíveis)

            action = "HOLD"
            if confidence >= 70:
                action = "BUY"
            elif confidence <= 30:
                action = "SELL"

            self.indicators[asset] = {"confidence": confidence, "action": action}

        self.logger.log(f"IndicatorIA: Indicadores atualizados: {self.indicators}")

    def get_indicator(self, asset):
        """
        Retorna indicador de um ativo específico.
        """
        return self.indicators.get(asset, {"confidence": 50, "action": "HOLD"})

    def get_status(self):
        """
        Retorna status atual da IA de indicadores.
        """
        return {"status": self.status, "indicators": self.indicators}
