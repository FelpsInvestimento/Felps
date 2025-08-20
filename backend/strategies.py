# backend/strategies.py
import random
from novadax_api import NovaDAXAPI

# IA 1 - Análise de Tendência
def ia_tendencia(symbol, prices):
    if prices[-1] > prices[0]:
        return "BUY"
    elif prices[-1] < prices[0]:
        return "SELL"
    return "HOLD"

# IA 2 - Análise de Volume
def ia_volume(symbol, volumes):
    if volumes[-1] > sum(volumes) / len(volumes) * 1.5:
        return "BUY"
    elif volumes[-1] < sum(volumes) / len(volumes) * 0.5:
        return "SELL"
    return "HOLD"

# IA 3 - RSI (Força Relativa)
def ia_rsi(symbol, prices, period=14):
    if len(prices) < period:
        return "HOLD"
    gains = []
    losses = []
    for i in range(1, len(prices)):
        diff = prices[i] - prices[i-1]
        if diff >= 0:
            gains.append(diff)
        else:
            losses.append(abs(diff))
    avg_gain = sum(gains) / period if gains else 0.0001
    avg_loss = sum(losses) / period if losses else 0.0001
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    if rsi < 30:
        return "BUY"
    elif rsi > 70:
        return "SELL"
    return "HOLD"

# IA 4 - Médias Móveis
def ia_media_movel(symbol, prices, short_window=5, long_window=20):
    if len(prices) < long_window:
        return "HOLD"
    short_ma = sum(prices[-short_window:]) / short_window
    long_ma = sum(prices[-long_window:]) / long_window
    if short_ma > long_ma:
        return "BUY"
    elif short_ma < long_ma:
        return "SELL"
    return "HOLD"

# IA 5 - Padrões de Velas (simplificado)
def ia_padroes_velas(symbol, candles):
    # candles = lista de tuplas (open, high, low, close)
    last = candles[-1]
    if last[3] > last[0] and (last[1] - last[2]) > (last[0] * 0.01):
        return "BUY"
    elif last[3] < last[0] and (last[1] - last[2]) > (last[0] * 0.01):
        return "SELL"
    return "HOLD"

# Função principal que combina as 5 IAs
def analyze_market(symbol, mode="moderado"):
    api = NovaDAXAPI("SUA_API_KEY", "SUA_API_SECRET")  # Troque pelas suas chaves
    prices = api.get_historical_prices(symbol)
    volumes = [p["volume"] for p in prices]
    closes = [p["close"] for p in prices]
    candles = [(p["open"], p["high"], p["low"], p["close"]) for p in prices]

    sinais = [
        ia_tendencia(symbol, closes),
        ia_volume(symbol, volumes),
        ia_rsi(symbol, closes),
        ia_media_movel(symbol, closes),
        ia_padroes_velas(symbol, candles)
    ]

    # Contagem dos sinais
    buy_count = sinais.count("BUY")
    sell_count = sinais.count("SELL")

    # Decisão com base no modo
    if mode == "leve":
        decisao = "BUY" if buy_count >= 3 else "SELL" if sell_count >= 3 else "HOLD"
    elif mode == "agressivo":
        decisao = "BUY" if buy_count >= 2 else "SELL" if sell_count >= 2 else "HOLD"
    else:  # moderado ou automático
        decisao = "BUY" if buy_count > sell_count else "SELL" if sell_count > buy_count else "HOLD"

    # Retorna a decisão e o último preço
    return decisao, closes[-1]
