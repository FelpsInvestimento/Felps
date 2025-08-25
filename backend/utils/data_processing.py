import pandas as pd
import numpy as np

class DataProcessing:
    def __init__(self):
        pass

    def process_market_data(self, raw_data):
        """
        Recebe dados brutos do mercado (lista de dicionários) e retorna DataFrame processado.
        Exemplo de raw_data:
        [
            {"symbol": "BTCUSDT", "price": "30000", "volume": "12.5", "timestamp": 1690000000},
            {"symbol": "ETHUSDT", "price": "2000", "volume": "150", "timestamp": 1690000000}
        ]
        """
        df = pd.DataFrame(raw_data)
        df['price'] = df['price'].astype(float)
        df['volume'] = df['volume'].astype(float)
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
        return df

    def calculate_moving_average(self, df, period=5):
        """
        Calcula média móvel simples para cada ativo.
        Retorna DataFrame com coluna 'ma_{period}'.
        """
        df = df.copy()
        df['ma_{}'.format(period)] = df.groupby('symbol')['price'].transform(lambda x: x.rolling(period).mean())
        return df

    def calculate_volatility(self, df, period=5):
        """
        Calcula volatilidade simples (desvio padrão) para cada ativo.
        Retorna DataFrame com coluna 'vol_{period}'.
        """
        df = df.copy()
        df['vol_{}'.format(period)] = df.groupby('symbol')['price'].transform(lambda x: x.rolling(period).std())
        return df

    def calculate_price_change(self, df):
        """
        Calcula variação percentual diária do preço.
        """
        df = df.copy()
        df['price_change'] = df.groupby('symbol')['price'].pct_change() * 100
        return df

    def filter_active_assets(self, df, min_volume=1.0):
        """
        Filtra apenas ativos com volume mínimo.
        """
        return df[df['volume'] >= min_volume]
