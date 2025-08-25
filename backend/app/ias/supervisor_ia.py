import time
from threading import Thread

from app.services.novadax_api import NovaDAXAPI
from app.ias.analysis_ia import AnalysisIA
from app.ias.buy_ia import BuyIA
from app.ias.sell_ia import SellIA
from app.ias.stop_loss_ia import StopLossIA

class SupervisorIA:
    def __init__(self, accounts_config):
        self.accounts = {}
        self.trading_mode = "AUTOMATIC" # Default mode
        self.is_running = False
        self.operations_log = []

        for acc_name, acc_details in accounts_config.items():
            api = NovaDAXAPI(access_key=acc_details["access_key"], secret_key=acc_details["secret_key"])
            self.accounts[acc_name] = {
                "api": api,
                "analysis_ia": AnalysisIA(api),
                "buy_ia": BuyIA(api),
                "sell_ia": SellIA(api),
                "stop_loss_ia": StopLossIA(api),
                "current_balance": {},
                "open_positions": {}, # {symbol: amount}
                "api_key_details": acc_details # Store details for display
            }

    def set_trading_mode(self, mode):
        if mode in ["LIGHT", "MODERATE", "AGGRESSIVE", "AUTOMATIC"]:
            self.trading_mode = mode
            print(f"Modo de negociação alterado para: {self.trading_mode}")
        else:
            print("Modo de negociação inválido.")

    def get_trading_mode(self):
        return self.trading_mode

    def get_all_balances(self):
        all_balances = {}
        for acc_name, acc_data in self.accounts.items():
            balance_response = acc_data["api"].get_balance()
            if balance_response and balance_response.get("code") == "A10000":
                acc_data["current_balance"] = {item["currency"]: float(item["available"]) for item in balance_response["data"]}
                all_balances[acc_name] = acc_data["current_balance"]
            else:
                all_balances[acc_name] = {"error": balance_response.get("message", "Erro ao obter saldo.")}
        return all_balances

    def get_operations_log(self):
        return self.operations_log

    def _log_operation(self, account, operation_type, symbol, details):
        log_entry = {
            "timestamp": time.time(),
            "account": account,
            "type": operation_type,
            "symbol": symbol,
            "details": details
        }
        self.operations_log.append(log_entry)
        print(f"[LOG] Conta: {account}, Tipo: {operation_type}, Símbolo: {symbol}, Detalhes: {details}")

    def _run_trading_logic(self, account_name, account_data):
        api = account_data["api"]
        analysis_ia = account_data["analysis_ia"]
        buy_ia = account_data["buy_ia"]
        sell_ia = account_data["sell_ia"]
        stop_loss_ia = account_data["stop_loss_ia"]

        # 1. Obter todos os símbolos negociáveis (pode ser feito uma vez ou periodicamente)
        tradable_symbols = analysis_ia.get_all_tradable_symbols()
        if not tradable_symbols:
            self._log_operation(account_name, "INFO", "N/A", "Não foi possível obter símbolos negociáveis.")
            return

        # 2. Iterar sobre os ativos e aplicar a lógica de trade
        for symbol in tradable_symbols:
            # Lógica para determinar quais ativos operar com base no modo
            # Ex: no modo LIGHT, operar apenas BTC_BRL, no AGGRESSIVE, operar tudo
            if self.trading_mode == "LIGHT" and symbol != "BTC_BRL":
                continue
            # Adicione mais lógica de modo aqui

            # Análise de mercado
            analysis_result = analysis_ia.analyze_market(symbol)
            self._log_operation(account_name, "ANALYSIS", symbol, analysis_result)

            if analysis_result["decision"] == "BUY_SIGNAL":
                # Lógica de compra
                # Determinar quantidade e preço de compra com base na confiança e saldo disponível
                # Exemplo simplificado: comprar uma pequena quantidade
                balance_data = self.get_all_balances().get(account_name, {})
                brl_balance = balance_data.get("BRL", 0.0)
                if brl_balance > 100: # Exemplo: ter pelo menos 100 BRL para operar
                    amount_to_buy = 10 / analysis_result["price"] # Comprar o equivalente a 10 BRL
                    buy_response = buy_ia.execute_buy_order(symbol, analysis_result["price"], amount_to_buy, account_id=account_name) # Usar account_name como account_id para subcontas
                    self._log_operation(account_name, "BUY", symbol, buy_response)
                    if buy_response["status"] == "SUCCESS":
                        # Atualizar posições abertas
                        account_data["open_positions"][symbol] = account_data["open_positions"].get(symbol, 0) + amount_to_buy
                else:
                    self._log_operation(account_name, "INFO", symbol, "Saldo insuficiente para compra.")

            # Monitorar posições abertas para Stop Loss
            if symbol in account_data["open_positions"] and account_data["open_positions"][symbol] > 0:
                entry_price = analysis_result["price"] # Idealmente, seria o preço médio de compra
                current_amount = account_data["open_positions"][symbol]
                stop_loss_result = stop_loss_ia.monitor_and_execute_stop_loss(symbol, entry_price, current_amount, account_id=account_name)
                self._log_operation(account_name, "STOP_LOSS_MONITOR", symbol, stop_loss_result)
                if stop_loss_result["status"] == "STOP_LOSS_EXECUTED":
                    account_data["open_positions"][symbol] = 0 # Posição fechada

            # Lógica de venda (take profit, etc.)
            # Isso seria mais complexo, envolvendo análise contínua da posição
            # Por exemplo, se o lucro atingir X%, vender.
            # if analysis_result["decision"] == "SELL_SIGNAL":
            #     if symbol in account_data["open_positions"] and account_data["open_positions"][symbol] > 0:
            #         sell_response = sell_ia.execute_sell_order(symbol, analysis_result["price"], account_data["open_positions"][symbol], account_id=account_name)
            #         self._log_operation(account_name, "SELL", symbol, sell_response)
            #         if sell_response["status"] == "SUCCESS":
            #             account_data["open_positions"][symbol] = 0

    def start_trading(self):
        if self.is_running:
            print("O robô já está em execução.")
            return

        self.is_running = True
        print("Iniciando o robô FELPS TRADE...")

        def trading_loop():
            while self.is_running:
                for account_name, account_data in self.accounts.items():
                    print(f"Executando lógica de trade para a conta: {account_name}")
                    self._run_trading_logic(account_name, account_data)
                time.sleep(60) # Executa a cada 60 segundos (ajustável)

        self.trading_thread = Thread(target=trading_loop)
        self.trading_thread.daemon = True # Permite que o programa principal saia mesmo que a thread esteja rodando
        self.trading_thread.start()

    def stop_trading(self):
        self.is_running = False
        if hasattr(self, 'trading_thread') and self.trading_thread.is_alive():
            self.trading_thread.join(timeout=5) # Espera a thread terminar
            print("Robô FELPS TRADE parado.")
        else:
            print("O robô não estava em execução.")

    def get_status(self):
        status = {
            "is_running": self.is_running,
            "trading_mode": self.trading_mode,
            "accounts_status": {}
        }
        for acc_name, acc_data in self.accounts.items():
            status["accounts_status"][acc_name] = {
                "balance": acc_data["current_balance"],
                "open_positions": acc_data["open_positions"],
                "api_key_details": {k: v for k, v in acc_data["api_key_details"].items() if k != "secret_key"} # Não expor secret_key
            }
        return status

    def check_ias_functioning(self):
        # Uma verificação mais robusta seria executar testes unitários ou simulações
        # Por enquanto, apenas um status baseado na execução do loop
        return {"status": "OK" if self.is_running else "INACTIVE", "message": "As IAs estão sendo invocadas no loop de negociação."}


# Exemplo de uso (para teste local)
if __name__ == "__main__":
    # Configuração de exemplo para múltiplas contas
    # Em um ambiente real, isso viria de um banco de dados ou arquivo de configuração seguro
    accounts_config = {
        "CONTA_1": {
            "access_key": "fb17caa1-00a5-45ad-800f-31dcff935376",
            "secret_key": "IDqP2LKyivmnBprsRQ8qzLt6oQPQNWGo"
        },
        # "CONTA_2": {
        #     "access_key": "OUTRA_ACCESS_KEY_2",
        #     "secret_key": "OUTRA_SECRET_KEY_2"
        # },
        # Adicione até 10 contas aqui
    }

    supervisor = SupervisorIA(accounts_config)

    # Iniciar o robô
    supervisor.start_trading()

    # Simular alguma interação após um tempo
    time.sleep(10) # Deixa o robô rodar por 10 segundos

    # Verificar saldo
    print("\nSaldo das contas:", supervisor.get_all_balances())

    # Verificar status das IAs
    print("\nStatus das IAs:", supervisor.check_ias_functioning())

    # Mudar modo de negociação
    supervisor.set_trading_mode("MODERATE")

    time.sleep(10) # Deixa o robô rodar por mais 10 segundos

    # Parar o robô
    supervisor.stop_trading()

    # Ver log de operações
    print("\nLog de Operações:")
    for log in supervisor.get_operations_log():
        print(log)


