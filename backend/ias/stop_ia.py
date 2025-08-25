import time
from utils.logger import Logger

class StopIA:
    def __init__(self, api_connector, interval=5):
        """
        Inicializa a IA de Stop Loss Inteligente.
        api_connector: Conector das contas da corretora
        interval: tempo em segundos entre verificações
        """
        self.api_connector = api_connector
        self.logger = Logger()
        self.interval = interval
        self.status = "Iniciando"
        self.stop_percent = 2  # Percentual padrão
        self.positions = {}  # Guarda posições monitoradas: { "account_name": { "asset": buy_price } }

    def start(self):
        """
        Inicia a verificação contínua de stop loss.
        """
        self.logger.log("StopIA iniciada")
        self.status = "Rodando"
        while True:
            try:
                self.run_stop()
            except Exception as e:
                self.logger.log(f"ERRO StopIA: {e}")
            time.sleep(self.interval)

    def set_stop_percent(self, percent):
        """
        Atualiza a porcentagem de stop loss.
        """
        self.stop_percent = percent
        self.logger.log(f"StopIA: Stop inteligente configurado para {percent}%")

    def update_positions(self, account_name, asset, buy_price):
        """
        Atualiza o preço de compra de um ativo para monitoramento.
        """
        if account_name not in self.positions:
            self.positions[account_name] = {}
        self.positions[account_name][asset] = buy_price

    def run_stop(self):
        """
        Verifica todas as posições e executa stop loss se necessário.
        """
        for account_name, assets in self.positions.items():
            for asset, buy_price in assets.items():
                balance = self.api_connector.get_balances().get(account_name, {})
                asset_amount = balance.get(asset, 0)
                if asset_amount <= 0:
                    continue

                # Obter preço atual (exemplo simplificado)
                current_price = self.get_current_price(asset)
                if current_price is None:
                    continue

                # Calcula variação percentual
                loss_percent = ((buy_price - current_price) / buy_price) * 100
                if loss_percent >= self.stop_percent:
                    # Executa venda para stop loss
                    response = self.api_connector.place_order(
                        account_name=account_name,
                        symbol=asset,
                        side='SELL',
                        quantity=asset_amount,
                        order_type='MARKET'
                    )
                    self.logger.log(f"StopIA: Stop Loss acionado para {asset} na {account_name} com {loss_percent:.2f}% de perda: {response}")
                    # Remove posição monitorada
                    del self.positions[account_name][asset]

    def get_current_price(self, asset):
        """
        Obtém o preço atual do ativo (simplificação: pega de primeira conta)
        """
        balances = self.api_connector.get_balances()
        for acc_name, assets in balances.items():
            if asset in assets:
                return assets[asset]  # Aqui você deve usar preço real da corretora
        return None

    def get_status(self):
        """
        Retorna status atual da IA de stop loss.
        """
        return {"status": self.status, "stop_percent": self.stop_percent, "positions_monitored": self.positions}
