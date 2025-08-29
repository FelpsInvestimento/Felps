import requests
import time
from datetime import datetime, timedelta

class SentimentAnalysisIA:
    def __init__(self, novadax_api):
        self.novadax_api = novadax_api
        self.last_news_check = None
        self.sentiment_cache = {}
        
    def get_crypto_news_sentiment(self, symbol):
        """
        Analisa o sentimento das notícias relacionadas ao ativo
        Retorna um score de -1 (muito negativo) a +1 (muito positivo)
        """
        try:
            # Extrair o nome da criptomoeda do símbolo (ex: BTC_BRL -> BTC)
            crypto_name = symbol.split('_')[0] if '_' in symbol else symbol
            
            # Verificar cache para evitar muitas requisições
            cache_key = f"{crypto_name}_{datetime.now().strftime('%Y%m%d%H')}"
            if cache_key in self.sentiment_cache:
                return self.sentiment_cache[cache_key]
            
            # Simular análise de sentimento (em produção, usaria APIs reais como NewsAPI, Alpha Vantage, etc.)
            sentiment_score = self._simulate_news_sentiment(crypto_name)
            
            # Armazenar no cache
            self.sentiment_cache[cache_key] = sentiment_score
            
            return sentiment_score
            
        except Exception as e:
            print(f"Erro na análise de sentimento para {symbol}: {e}")
            return 0.0  # Neutro em caso de erro
    
    def _simulate_news_sentiment(self, crypto_name):
        """
        Simula análise de sentimento de notícias
        Em produção, isso seria substituído por chamadas reais para APIs de notícias
        """
        # Simulação baseada em padrões de mercado conhecidos
        import random
        
        # Fatores que influenciam o sentimento
        factors = {
            'BTC': 0.1,    # Bitcoin geralmente tem sentimento mais positivo
            'ETH': 0.05,   # Ethereum também positivo
            'BNB': 0.0,    # Neutro
            'ADA': -0.05,  # Ligeiramente negativo
            'DOGE': 0.15,  # Meme coins têm volatilidade alta no sentimento
        }
        
        base_sentiment = factors.get(crypto_name, 0.0)
        
        # Adicionar variação aleatória para simular notícias do dia
        daily_variation = random.uniform(-0.3, 0.3)
        
        # Calcular sentimento final
        final_sentiment = max(-1.0, min(1.0, base_sentiment + daily_variation))
        
        return final_sentiment
    
    def get_market_sentiment_summary(self, symbols_list):
        """
        Retorna um resumo do sentimento geral do mercado
        """
        if not symbols_list:
            return {"overall_sentiment": 0.0, "sentiment_strength": "neutral"}
        
        sentiments = []
        for symbol in symbols_list[:10]:  # Limitar a 10 símbolos para performance
            sentiment = self.get_crypto_news_sentiment(symbol)
            sentiments.append(sentiment)
        
        if not sentiments:
            return {"overall_sentiment": 0.0, "sentiment_strength": "neutral"}
        
        overall_sentiment = sum(sentiments) / len(sentiments)
        
        # Classificar a força do sentimento
        if overall_sentiment > 0.3:
            strength = "very_positive"
        elif overall_sentiment > 0.1:
            strength = "positive"
        elif overall_sentiment > -0.1:
            strength = "neutral"
        elif overall_sentiment > -0.3:
            strength = "negative"
        else:
            strength = "very_negative"
        
        return {
            "overall_sentiment": overall_sentiment,
            "sentiment_strength": strength,
            "analyzed_symbols": len(sentiments),
            "timestamp": datetime.now().isoformat()
        }
    
    def should_trade_based_on_sentiment(self, symbol, trading_mode="AUTOMATIC"):
        """
        Determina se deve negociar baseado no sentimento das notícias
        """
        sentiment_score = self.get_crypto_news_sentiment(symbol)
        
        # Thresholds baseados no modo de trading
        thresholds = {
            "LIGHT": {"buy": 0.4, "sell": -0.4},
            "MODERATE": {"buy": 0.2, "sell": -0.2},
            "AGGRESSIVE": {"buy": 0.1, "sell": -0.1},
            "AUTOMATIC": {"buy": 0.15, "sell": -0.15}
        }
        
        mode_threshold = thresholds.get(trading_mode, thresholds["AUTOMATIC"])
        
        if sentiment_score >= mode_threshold["buy"]:
            return {
                "action": "BUY",
                "confidence": min(abs(sentiment_score), 1.0),
                "sentiment_score": sentiment_score,
                "reason": f"Sentimento positivo das notícias ({sentiment_score:.2f})"
            }
        elif sentiment_score <= mode_threshold["sell"]:
            return {
                "action": "SELL",
                "confidence": min(abs(sentiment_score), 1.0),
                "sentiment_score": sentiment_score,
                "reason": f"Sentimento negativo das notícias ({sentiment_score:.2f})"
            }
        else:
            return {
                "action": "HOLD",
                "confidence": 0.5,
                "sentiment_score": sentiment_score,
                "reason": f"Sentimento neutro das notícias ({sentiment_score:.2f})"
            }
    
    def get_sentiment_report(self, symbols_list):
        """
        Gera um relatório detalhado do sentimento para múltiplos ativos
        """
        report = {
            "timestamp": datetime.now().isoformat(),
            "symbols_analyzed": [],
            "market_summary": self.get_market_sentiment_summary(symbols_list)
        }
        
        for symbol in symbols_list[:5]:  # Limitar para performance
            sentiment_data = {
                "symbol": symbol,
                "sentiment_score": self.get_crypto_news_sentiment(symbol),
                "recommendation": self.should_trade_based_on_sentiment(symbol)
            }
            report["symbols_analyzed"].append(sentiment_data)
        
        return report


# Exemplo de uso e teste
if __name__ == "__main__":
    # Para teste, criar uma instância mock da API
    class MockAPI:
        pass
    
    sentiment_ia = SentimentAnalysisIA(MockAPI())
    
    # Testar análise de sentimento
    test_symbols = ["BTC_BRL", "ETH_BRL", "ADA_BRL"]
    
    print("=== TESTE DA IA DE ANÁLISE DE SENTIMENTO ===")
    
    for symbol in test_symbols:
        sentiment = sentiment_ia.get_crypto_news_sentiment(symbol)
        recommendation = sentiment_ia.should_trade_based_on_sentiment(symbol)
        
        print(f"\n{symbol}:")
        print(f"  Sentimento: {sentiment:.3f}")
        print(f"  Recomendação: {recommendation['action']}")
        print(f"  Confiança: {recommendation['confidence']:.3f}")
        print(f"  Razão: {recommendation['reason']}")
    
    # Testar resumo do mercado
    market_summary = sentiment_ia.get_market_sentiment_summary(test_symbols)
    print(f"\n=== RESUMO DO MERCADO ===")
    print(f"Sentimento Geral: {market_summary['overall_sentiment']:.3f}")
    print(f"Força: {market_summary['sentiment_strength']}")
    
    # Testar relatório completo
    report = sentiment_ia.get_sentiment_report(test_symbols)
    print(f"\n=== RELATÓRIO COMPLETO ===")
    print(f"Símbolos analisados: {len(report['symbols_analyzed'])}")
    print(f"Sentimento do mercado: {report['market_summary']['sentiment_strength']}")

