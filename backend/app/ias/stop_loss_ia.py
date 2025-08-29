import time

class StopLossIA:
    def __init__(self, novadax_api):
        self.novadax_api = novadax_api

    def calculate_stop_loss_price(self, entry_price, stop_percentage):
        """
        Calcula o preço do stop loss com base na porcentagem configurada.
        """
        return entry_price * (1 - stop_percentage)

    def monitor_and_execute_stop_loss(self, symbol, entry_price, current_amount, current_price, stop_percentage, account_id=None, allow_dynamic_stop_loss=True):
        """
        Monitora o preço atual e executa o stop loss se necessário.
        Permite ajuste dinâmico do stop loss.
        """
        calculated_stop_price = self.calculate_stop_loss_price(entry_price, stop_percentage)

        # Lógica para trailing stop ou ajuste dinâmico
        # Se o preço subiu significativamente, podemos mover o stop loss para proteger lucros
        if allow_dynamic_stop_loss and current_price > entry_price:
            profit_percentage = ((current_price - entry_price) / entry_price)
            # Se o lucro for maior que o stop loss original, move o stop para o ponto de equilíbrio ou acima
            if profit_percentage > stop_percentage:
                # Move o stop para um pouco abaixo do preço atual para travar lucro
                dynamic_stop_price = current_price * (1 - (stop_percentage / 2)) # Ex: metade da porcentagem original
                calculated_stop_price = max(calculated_stop_price, dynamic_stop_price)

        if current_price <= calculated_stop_price:
            print(f"[STOP LOSS] Ativado para {symbol}. Preço atual: {current_price}, Preço de Stop: {calculated_stop_price}")
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
            return {"status": "MONITORING", "message": "Preço acima do Stop Loss.", "current_price": current_price, "stop_price": calculated_stop_price}


