import time
from utils.logger import Logger

class SellIA:
    def __init__(self, api_connector, interval=5):
        """
        Inicializa a IA de venda.
        api_connector: Conector das contas da corretora
        interval: tempo em segundos entre verificações de venda
        """
        self.api_connector = api_connector
        self.logger = Logger()
        self.interval = interval
        self.status = "Iniciando"
        self.assets_to_sell = []

    def start(self):
        """
        Inicia a execução contínua de vendas.
        """
        self.logger.log("SellIA iniciada")
        self.status = "Rodando"
        while True:
            try:
                self.run_sell()
            except Exception as e:
                self.logger.log(f"ERRO SellIA: {e}")
            time.sleep(self.interval)

    def set_assets(self, assets):
        """
        Recebe a lista de ativos para venda.
        """
        self.assets_to_sell = assets

    def run_sell(self):
        """
        Executa vendas para todos os ativos definidos.
        """
        if not self.assets_to_sell:
            return

        for asset in self.assets_to_sell:
            for account in self.api_connector.accounts:
                try:
                    balance = self.api_connector.get_balances().get(account['name'], {})
                    asset_amount = balance.get(asset, 0)
                    if asset_amount <= 0:
                        self.logger.log(f"Nenhum {asset} disponível na {account['name']} para vender")
                        continue

                    response = self.api_connector.place_order(
                        account_name=account['name'],
                        symbol=asset,
                        side='SELL',
                        quantity=asset_amount,
                        order_type='MARKET'
                    )
                    self.logger.log(f"SellIA: Venda de {asset} na {account['name']} executada: {response}")
                except Exception as e:
                    self.logger.log(f"ERRO SellIA ao vender {asset} na {account['name']}: {e}")

    def get_status(self):
        """
        Retorna status atual da IA de venda.
        """
        return {"status": self.status, "assets_to_sell": self.assets_to_sell}
