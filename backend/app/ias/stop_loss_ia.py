class StopLossIA:
    def __init__(self, novadax_api):
        self.novadax_api = novadax_api

    def calculate_stop_loss(self, current_price, entry_price, stop_percentage=0.02): # 2% padrão
        # Lógica para calcular o preço do stop loss
        # Pode ser um stop fixo ou trailing stop
        # Aqui, um stop fixo baseado na porcentagem de perda máxima
        
        # Se for uma posição de compra, o stop loss é abaixo do preço de entrada
        # Se for uma posição de venda (short), o stop loss é acima do preço de entrada
        
        # Simplificado para o exemplo: stop loss de saída de 1% a 2% do preço atual
        # O usuário especificou 1% a 2% de stop de saída. Isso pode ser interpretado como
        # um stop loss que se move com o preço (trailing stop) ou um stop fixo.
        # Vamos implementar um stop fixo baseado no preço de entrada para simplificar.
        
        # Para uma posição de compra, o stop loss é (1 - porcentagem) * preço de entrada
        # Para uma posição de venda, o stop loss é (1 + porcentagem) * preço de entrada
        
        # Considerando que o robô está comprando e vendendo, o stop loss será para proteger a compra.
        # Ou seja, se o preço cair X% da entrada, vende.
        
        stop_price = entry_price * (1 - stop_percentage)
        return stop_price

    def monitor_and_execute_stop_loss(self, symbol, entry_price, current_amount, account_id=None):
        # Monitora o preço atual e executa o stop loss se necessário
        stop_percentage = 0.02 # Exemplo: 2% de stop
        stop_price = self.calculate_stop_loss(None, entry_price, stop_percentage)

        ticker_data = self.novadax_api.get_ticker(symbol)
        if ticker_data and ticker_data.get("code") == "A10000":
            current_market_price = float(ticker_data["data"]["lastPrice"])

            if current_market_price <= stop_price:
                print(f"[STOP LOSS] Ativado para {symbol}. Preço atual: {current_market_price}, Preço de Stop: {stop_price}")
                # Executar ordem de venda a mercado para sair da posição
                response = self.novadax_api.create_order(
                    symbol=symbol,
                    side="SELL",
                    order_type="MARKET", # Ordem a mercado para garantir a saída
                    size=current_amount, # Vende toda a quantidade
                    account_id=account_id
                )
                if response and response.get("code") == "A10000":
                    return {"status": "STOP_LOSS_EXECUTED", "order_info": response["data"], "message": "Stop Loss executado com sucesso."}
                else:
                    return {"status": "STOP_LOSS_FAILED", "message": response.get("message", "Erro ao executar Stop Loss."), "error_details": response}
            else:
                return {"status": "MONITORING", "message": "Preço acima do Stop Loss.", "current_price": current_market_price, "stop_price": stop_price}
        return {"status": "ERROR", "message": "Não foi possível obter o preço atual para monitoramento de Stop Loss."}


