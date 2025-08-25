import time
from utils.logger import Logger

class BuyIA:
    def __init__(self, api_connector, interval=5):
        """
        Inicializa a IA de compra.
        api_connector: Conector das contas da corretora
        interval: tempo em segundos entre tentativas de compra
        """
        self.api_connector = api_connector
        self.logger = Logger()
        self.interval = interval
        self.status = "Iniciando"
        self.assets_to_buy = []

    def start(self):
        """
        Inicia a execução contínua de compras.
        """
        self.logger.log("BuyIA iniciada")
        self.status = "Rodando"
        while True:
            try:
                self.run_buy()
            except Exception as e:
                self.logger.log(f"ERRO BuyIA: {e}")
            time.sleep(self.interval)

    def set_assets(self, assets):
        """
        Recebe a lista de ativos para compra.
        """
        self.assets_to_buy = assets

    def run_buy(self):
        """
        Executa compras para todos os ativos definidos.
        """
        if not self.assets_to_buy:
            return

        for asset in self.assets_to_buy:
            for account in self.api_connector.accounts:
                try:
                    balance = self.api_connector.get_balances().get(account['name'], {})
                    usdt_balance = balance.get("USDT", 0)
                    if usdt_balance < 10:  # Verificação mínima para compra
                        self.logger.log(f"Saldo insuficiente na {account['name']} para comprar {asset}")
                        continue

                    # Definindo quantidade proporcional ao saldo disponível
                    quantity = round(usdt_balance / 10, 6)  # Exemplo: divide o saldo em 10 partes
                    response = self.api_connector.place_order(
                        account_name=account['name'],
                        symbol=asset,
                        side='BUY',
                        quantity=quantity,
                        order_type='MARKET'
                    )
                    self.logger.log(f"BuyIA: Compra de {asset} na {account['name']} executada: {response}")
                except Exception as e:
                    self.logger.log(f"ERRO BuyIA ao comprar {asset} na {account['name']}: {e}")

    def get_status(self):
        """
        Retorna status atual da IA de compra.
        """
        return {"status": self.status, "assets_to_buy": self.assets_to_buy}
