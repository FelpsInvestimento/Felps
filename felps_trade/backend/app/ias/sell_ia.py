class SellIA:
    def __init__(self, novadax_api):
        self.novadax_api = novadax_api

    def execute_sell_order(self, symbol, price, amount, account_id=None):
        # Lógica para executar uma ordem de venda
        # Pode ser uma ordem a mercado ou limitada, dependendo da estratégia
        order_type = "LIMIT" # Exemplo: ordem limitada
        side = "SELL"

        # Validação básica para evitar ordens inválidas
        if not symbol or not price or not amount or amount <= 0:
            return {"status": "ERROR", "message": "Parâmetros de venda inválidos."}

        # Chamar a API da NovaDAX para criar a ordem
        response = self.novadax_api.create_order(
            symbol=symbol,
            side=side,
            order_type=order_type,
            size=amount,
            price=price,
            account_id=account_id
        )

        if response and response.get("code") == "A10000":
            return {"status": "SUCCESS", "order_info": response["data"], "message": "Ordem de venda executada com sucesso."}
        else:
            return {"status": "FAILED", "message": response.get("message", "Erro desconhecido ao executar ordem de venda."), "error_details": response}


