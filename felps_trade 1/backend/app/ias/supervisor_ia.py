import time
from threading import Thread

from app.services.novadax_api import NovaDAXAPI
from app.ias.analysis_ia import AnalysisIA
from app.ias.buy_ia import BuyIA
from app.ias.sell_ia import SellIA
from app.ias.stop_loss_ia import StopLossIA
from app.ias.sentiment_analysis_ia import SentimentAnalysisIA
from app.ias.profit_optimization_ia import ProfitOptimizationIA

class SupervisorIA:
    def __init__(self, accounts_config, initial_settings=None):
        self.accounts = {}
        self.trading_mode = "AUTOMATIC" # Default mode
        self.is_running = False
        self.operations_log = []
        self.global_settings = {
            "daily_profit_target": None, # Meta de lucro diário global
            "custom_entry_value": None,  # Valor de entrada customizado global
            "stop_loss_percentage": 0.02, # Porcentagem de stop loss global (2% padrão)
            "selected_assets": [],       # Ativos selecionados manualmente
            "allow_dynamic_stop_loss": True # Permitir mudança de stop em operação
        }

        if initial_settings:
            self.global_settings.update(initial_settings)

        for acc_name, acc_details in accounts_config.items():
            api = NovaDAXAPI(access_key=acc_details["access_key"], secret_key=acc_details["secret_key"])
            self.accounts[acc_name] = {
                "api": api,
                "analysis_ia": AnalysisIA(api),
                "buy_ia": BuyIA(api),
                "sell_ia": SellIA(api),
                "stop_loss_ia": StopLossIA(api),
                "sentiment_analysis_ia": SentimentAnalysisIA(api),
                "profit_optimization_ia": ProfitOptimizationIA(api),
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
        sentiment_analysis_ia = account_data["sentiment_analysis_ia"]
        profit_optimization_ia = account_data["profit_optimization_ia"]

        # Obter configurações globais
        daily_profit_target = self.global_settings["daily_profit_target"]
        custom_entry_value = self.global_settings["custom_entry_value"]
        global_stop_loss_percentage = self.global_settings["stop_loss_percentage"]
        selected_assets = self.global_settings["selected_assets"]
        allow_dynamic_stop_loss = self.global_settings["allow_dynamic_stop_loss"]

        # 1. Obter todos os símbolos negociáveis
        tradable_symbols = analysis_ia.get_all_tradable_symbols()
        if not tradable_symbols:
            self._log_operation(account_name, "INFO", "N/A", "Não foi possível obter símbolos negociáveis.")
            return

        # Filtrar ativos se houver seleção manual
        if selected_assets:
            tradable_symbols = [s for s in tradable_symbols if s in selected_assets]

        # 2. Iterar sobre os ativos e aplicar a lógica de trade
        for symbol in tradable_symbols:
            # Lógica para determinar quais ativos operar com base no modo
            if self.trading_mode == "LIGHT" and symbol != "BTC_BRL":
                continue

            # Análise de mercado
            analysis_result = analysis_ia.analyze_market(symbol)
            self._log_operation(account_name, "ANALYSIS", symbol, analysis_result)

            # Análise de Sentimento de Notícias
            sentiment_result = sentiment_analysis_ia.should_trade_based_on_sentiment(symbol, self.trading_mode)
            self._log_operation(account_name, "SENTIMENT_ANALYSIS", symbol, sentiment_result)

            # Obter saldo atual
            balance_data = self.get_all_balances().get(account_name, {})
            brl_balance = balance_data.get("BRL", 0.0)

            # Decisão de Compra
            if analysis_result["decision"] == "BUY_SIGNAL" and sentiment_result["action"] == "BUY":
                # Calcular valor de entrada ótimo
                entry_calc = profit_optimization_ia.calculate_optimal_entry_amount(
                    symbol, brl_balance, self.trading_mode, custom_entry_value
                )
                amount_to_buy = entry_calc["entry_amount"] / analysis_result["price"]

                if brl_balance >= entry_calc["entry_amount"] and amount_to_buy > 0.0001: # Mínimo para NovaDAX
                    buy_response = buy_ia.execute_buy_order(symbol, analysis_result["price"], amount_to_buy, account_id=account_name)
                    self._log_operation(account_name, "BUY", symbol, buy_response)
                    if buy_response["status"] == "SUCCESS":
                        account_data["open_positions"][symbol] = {
                            "amount": account_data["open_positions"].get(symbol, {}).get("amount", 0) + amount_to_buy,
                            "entry_price": analysis_result["price"],
                            "timestamp": time.time()
                        }
                        profit_optimization_ia.update_trade_history({
                            "symbol": symbol, "action": "BUY", "entry_price": analysis_result["price"],
                            "position_size": amount_to_buy
                        })
                else:
                    self._log_operation(account_name, "INFO", symbol, "Saldo insuficiente ou valor de entrada muito baixo para compra.")

            # Monitorar posições abertas para Stop Loss e Otimização de Lucro
            if symbol in account_data["open_positions"] and account_data["open_positions"][symbol]["amount"] > 0:
                entry_price = account_data["open_positions"][symbol]["entry_price"]
                current_amount = account_data["open_positions"][symbol]["amount"]
                current_price = analysis_ia.get_current_price(symbol)

                # Gerenciamento de Stop Loss
                stop_loss_result = stop_loss_ia.monitor_and_execute_stop_loss(
                    symbol, entry_price, current_amount, current_price, global_stop_loss_percentage, account_id=account_name, 
                    allow_dynamic_stop_loss=allow_dynamic_stop_loss
                )
                self._log_operation(account_name, "STOP_LOSS_MONITOR", symbol, stop_loss_result)
                if stop_loss_result["status"] == "STOP_LOSS_EXECUTED":
                    account_data["open_positions"][symbol]["amount"] = 0
                    profit_optimization_ia.update_trade_history({
                        "symbol": symbol, "action": "SELL_STOP_LOSS", "entry_price": entry_price,
                        "exit_price": current_price, "position_size": current_amount,
                        "profit": (current_price - entry_price) * current_amount,
                        "profit_percentage": ((current_price - entry_price) / entry_price) * 100
                    })
                    continue # Posição fechada, ir para o próximo ativo

                # Otimização de Lucro (Take Profit)
                exit_strategy = profit_optimization_ia.calculate_optimal_exit_strategy(
                    symbol, entry_price, current_price, current_amount, daily_profit_target
                )
                self._log_operation(account_name, "PROFIT_OPTIMIZATION", symbol, exit_strategy)

                if exit_strategy["action"] == "SELL":
                    sell_response = sell_ia.execute_sell_order(symbol, current_price, current_amount, account_id=account_name)
                    self._log_operation(account_name, "SELL_TAKE_PROFIT", symbol, sell_response)
                    if sell_response["status"] == "SUCCESS":
                        account_data["open_positions"][symbol]["amount"] = 0
                        profit_optimization_ia.update_trade_history({
                            "symbol": symbol, "action": "SELL_TAKE_PROFIT", "entry_price": entry_price,
                            "exit_price": current_price, "position_size": current_amount,
                            "profit": (current_price - entry_price) * current_amount,
                            "profit_percentage": ((current_price - entry_price) / entry_price) * 100
                        })
                elif exit_strategy["action"] == "PARTIAL_SELL":
                    sell_percentage = exit_strategy["sell_percentage"] / 100
                    amount_to_sell = current_amount * sell_percentage
                    sell_response = sell_ia.execute_sell_order(symbol, current_price, amount_to_sell, account_id=account_name)
                    self._log_operation(account_name, "PARTIAL_SELL_TAKE_PROFIT", symbol, sell_response)
                    if sell_response["status"] == "SUCCESS":
                        account_data["open_positions"][symbol]["amount"] -= amount_to_sell
                        profit_optimization_ia.update_trade_history({
                            "symbol": symbol, "action": "PARTIAL_SELL_TAKE_PROFIT", "entry_price": entry_price,
                            "exit_price": current_price, "position_size": amount_to_sell,
                            "profit": (current_price - entry_price) * amount_to_sell,
                            "profit_percentage": ((current_price - entry_price) / entry_price) * 100
                        })

    def start_trading(self):
        if self.is_running:
            print("O robô já está em execução.")
            return

        self.is_running = True
        print("Iniciando o robô FELPS TRADE...")

        def trading_loop():
            while self.is_running:
                # Verificar se deve continuar operando com base na meta de lucro diário
                if self.global_settings["daily_profit_target"] is not None:
                    # Calcular lucro diário atual (simplificado para exemplo)
                    current_daily_profit = sum(t["profit"] for t in self.operations_log if t["type"] in ["SELL_TAKE_PROFIT", "PARTIAL_SELL_TAKE_PROFIT"] and time.time() - t["timestamp"] < 86400)
                    continue_trading_check = self.accounts[list(self.accounts.keys())[0]]["profit_optimization_ia"].should_continue_trading(
                        self.global_settings["daily_profit_target"], current_daily_profit
                    )
                    if not continue_trading_check["continue"]:
                        self._log_operation("GLOBAL", "INFO", "N/A", f"Parando trading: {continue_trading_check["reason"]}")
                        self.stop_trading()
                        break

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
            "global_settings": self.global_settings,
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
        return {"status": "OK" if self.is_running else "INACTIVE", "message": "As IAs estão sendo invocadas no loop de negociação."}

    def update_global_settings(self, settings):
        self.global_settings.update(settings)
        print(f"Configurações globais atualizadas: {self.global_settings}")


# Exemplo de uso (para teste local)
if __name__ == "__main__":
    # Configuração de exemplo para múltiplas contas
    accounts_config = {
        "CONTA_1": {
            "access_key": "fb17caa1-00a5-45ad-800f-31dcff935376",
            "secret_key": "IDqP2LKyivmnBprsRQ8qzLt6oQPQNWGo"
        },
    }

    # Exemplo de configurações iniciais
    initial_settings = {
        "daily_profit_target": 100.0, # R$ 100 de meta diária
        "custom_entry_value": 50.0,   # Entradas de R$ 50
        "stop_loss_percentage": 0.03, # Stop loss de 3%
        "selected_assets": ["BTC_BRL", "ETH_BRL"], # Operar apenas BTC e ETH
        "allow_dynamic_stop_loss": True
    }

    supervisor = SupervisorIA(accounts_config, initial_settings)

    # Iniciar o robô
    supervisor.start_trading()

    time.sleep(10) # Deixa o robô rodar por 10 segundos

    # Verificar saldo
    print("\nSaldo das contas:", supervisor.get_all_balances())

    # Verificar status das IAs
    print("\nStatus das IAs:", supervisor.check_ias_functioning())

    # Mudar modo de negociação
    supervisor.set_trading_mode("MODERATE")

    # Atualizar configurações globais em tempo de execução
    supervisor.update_global_settings({"stop_loss_percentage": 0.01, "selected_assets": []})

    time.sleep(10) # Deixa o robô rodar por mais 10 segundos

    # Parar o robô
    supervisor.stop_trading()

    # Ver log de operações
    print("\nLog de Operações:")
    for log in supervisor.get_operations_log():
        print(log)

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


