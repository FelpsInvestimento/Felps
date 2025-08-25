import time
from utils.data_processing import DataProcessing
from utils.logger import Logger

class AnalysisIA:
    def __init__(self, api_connector, interval=5):
        """
        Inicializa a IA de análise de ativos.
        api_connector: Conector das contas da corretora
        interval: tempo em segundos entre análises
        """
        self.api_connector = api_connector
        self.dp = DataProcessing()
        self.logger = Logger()
        self.interval = interval
        self.status = "Iniciando"
        self.best_assets = []

    def start(self):
        """
        Inicia a análise contínua em loop.
        """
        self.logger.log("AnalysisIA iniciada")
        self.status = "Rodando"
        while True:
            try:
                self.run_analysis()
            except Exception as e:
                self.logger.log(f"ERRO AnalysisIA: {e}")
            time.sleep(self.interval)

    def run_analysis(self):
        """
        Roda uma análise dos ativos de todas as contas.
        """
        balances = self.api_connector.get_balances()
        all_assets = []
        for acc_name, assets in balances.items():
            for symbol, value in assets.items():
                all_assets.append({
                    "symbol": symbol,
                    "price": value,  # Aqui podemos obter preço real pela API
                    "volume": value  # Aqui podemos obter volume real pela API
                })

        # Processa os dados
        df = self.dp.process_market_data(all_assets)
        df = self.dp.calculate_price_change(df)
        df = self.dp.filter_active_assets(df, min_volume=0.001)

        # Seleciona os ativos mais promissores
        self.best_assets = df.sort_values(by='price_change', ascending=False).head(10)['symbol'].tolist()
        self.logger.log(f"Melhores ativos identificados: {self.best_assets}")

    def get_status(self):
        """
        Retorna status atual e ativos selecionados.
        """
        return {"status": self.status, "best_assets": self.best_assets}
