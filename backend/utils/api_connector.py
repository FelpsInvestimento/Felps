import requests
import hmac
import hashlib
import time
from config import CONFIG

class APIConnector:
    def __init__(self, api_keys):
        """
        Inicializa o conector com todas as contas.
        api_keys: lista de dicionários com 'name', 'access_key', 'secret_key'
        """
        self.accounts = api_keys

    def _sign_request(self, secret_key, payload):
        """
        Assina a requisição para a corretora.
        """
        query_string = '&'.join([f"{k}={v}" for k, v in payload.items()])
        signature = hmac.new(secret_key.encode(), query_string.encode(), hashlib.sha256).hexdigest()
        return signature

    def get_balances(self):
        """
        Retorna o saldo disponível de todas as contas.
        Exemplo de retorno:
        {
            "Conta 1": {"BTC": 0.5, "USDT": 1000},
            "Conta 2": {"BTC": 0.1, "USDT": 500},
        }
        """
        balances = {}
        for acc in self.accounts:
            # Aqui você coloca a URL real da API da corretora para saldo
            # Exemplo fictício:
            url = "https://api.sua-corretora.com/v1/account/balance"
            payload = {"timestamp": int(time.time() * 1000)}
            signature = self._sign_request(acc['secret_key'], payload)
            payload['signature'] = signature
            headers = {"X-API-KEY": acc['access_key']}
            try:
                response = requests.get(url, params=payload, headers=headers, timeout=5)
                data = response.json()
                # Adaptar conforme retorno da corretora
                balances[acc['name']] = {item['asset']: float(item['free']) for item in data['balances']}
            except Exception as e:
                balances[acc['name']] = {"error": str(e)}
        return balances

    def place_order(self, account_name, symbol, side, quantity, price=None, order_type='MARKET'):
        """
        Executa ordens de compra ou venda.
        side: 'BUY' ou 'SELL'
        order_type: 'MARKET' ou 'LIMIT'
        """
        acc = next((a for a in self.accounts if a['name'] == account_name), None)
        if not acc:
            return {"error": "Conta não encontrada"}

        url = "https://api.sua-corretora.com/v1/order"
        payload = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity,
            "timestamp": int(time.time() * 1000)
        }
        if price and order_type == 'LIMIT':
            payload['price'] = price

        signature = self._sign_request(acc['secret_key'], payload)
        payload['signature'] = signature
        headers = {"X-API-KEY": acc['access_key']}
        try:
            response = requests.post(url, params=payload, headers=headers, timeout=5)
            return response.json()
        except Exception as e:
            return {"error": str(e)}
