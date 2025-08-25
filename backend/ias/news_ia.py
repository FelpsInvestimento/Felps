import time
import requests
from utils.logger import Logger

class NewsIA:
    def __init__(self, interval=300):
        """
        Inicializa a IA de notícias.
        interval: tempo em segundos entre verificações
        """
        self.logger = Logger()
        self.interval = interval
        self.status = "Iniciando"
        self.sentiment_data = {}  # Ex: { "BTC": "positivo" }

    def start(self):
        """
        Inicia a verificação contínua de notícias.
        """
        self.logger.log("NewsIA iniciada")
        self.status = "Rodando"
        while True:
            try:
                self.run_news_analysis()
            except Exception as e:
                self.logger.log(f"ERRO NewsIA: {e}")
            time.sleep(self.interval)

    def run_news_analysis(self):
        """
        Busca notícias e avalia sentimento por ativo.
        """
        news_sources = [
            "https://api.exemplo.com/news/crypto",  # Substituir pela API real
        ]
        for source in news_sources:
            try:
                response = requests.get(source, timeout=10)
                data = response.json()
                for item in data.get("articles", []):
                    symbol = item.get("symbol")
                    sentiment = self.analyze_sentiment(item.get("title", "") + " " + item.get("description", ""))
                    if symbol:
                        self.sentiment_data[symbol] = sentiment
                self.logger.log(f"NewsIA: Atualizado sentimento de {len(self.sentiment_data)} ativos")
            except Exception as e:
                self.logger.log(f"ERRO NewsIA ao buscar notícias: {e}")

    def analyze_sentiment(self, text):
        """
        Avalia sentimento do texto: positivo, neutro ou negativo
        (Exemplo simplificado usando palavras-chave)
        """
        text_lower = text.lower()
        positive_words = ["alta", "cresce", "positivo", "lucro", "bom"]
        negative_words = ["queda", "perda", "negativo", "ruim", "desvalorização"]

        score = 0
        for word in positive_words:
            if word in text_lower:
                score += 1
        for word in negative_words:
            if word in text_lower:
                score -= 1

        if score > 0:
            return "positivo"
        elif score < 0:
            return "negativo"
        else:
            return "neutro"

    def get_sentiment(self, symbol):
        """
        Retorna o sentimento atual de um ativo.
        """
        return self.sentiment_data.get(symbol, "neutro")

    def get_status(self):
        """
        Retorna status atual da IA de notícias.
        """
        return {"status": self.status, "sentiment_data": self.sentiment_data}
