import requests
import hmac
import hashlib
import time
import base64
import json
from urllib.parse import urlencode

from app.utils.config import Config

class NovaDAXAPI:
    BASE_URL = "https://api.novadax.com"

    def __init__(self, access_key=None, secret_key=None):
        self.access_key = access_key if access_key else Config.NOVADAX_ACCESS_KEY
        self.secret_key = secret_key if secret_key else Config.NOVADAX_SECRET_KEY

        if not self.access_key or not self.secret_key:
            raise ValueError("As chaves de API da NovaDAX (Access Key e Secret Key) devem ser fornecidas ou configuradas nas variáveis de ambiente.")

    def _generate_signature(self, method, path, timestamp, query_string=None, body_md5=None):
        sign_str = f"{method}\n{path}\n"
        if query_string:
            sign_str += f"{query_string}\n"
        elif body_md5:
            sign_str += f"{body_md5}\n"
        sign_str += f"{timestamp}"

        h = hmac.new(self.secret_key.encode("utf-8"), sign_str.encode("utf-8"), hashlib.sha256)
        return base64.b64encode(h.digest()).decode("utf-8")

    def _send_request(self, method, path, params=None, data=None):
        timestamp = str(int(time.time() * 1000))
        headers = {
            "X-Nova-Access-Key": self.access_key,
            "X-Nova-Timestamp": timestamp,
            "Content-Type": "application/json" if data else "application/x-www-form-urlencoded"
        }

        query_string = None
        body_md5 = None

        if method == "GET" and params:
            query_string = urlencode(sorted(params.items()))
            full_path = f"{path}?{query_string}"
        else:
            full_path = path

        if data:
            body_md5 = hashlib.md5(json.dumps(data).encode("utf-8")).hexdigest()

        signature = self._generate_signature(method, path, timestamp, query_string, body_md5)
        headers["X-Nova-Signature"] = signature

        url = f"{self.BASE_URL}{full_path}"

        try:
            if method == "GET":
                response = requests.get(url, headers=headers)
            elif method == "POST":
                response = requests.post(url, headers=headers, json=data)
            else:
                raise ValueError("Método HTTP não suportado.")

            response.raise_for_status()  # Levanta um HTTPError para códigos de status de erro (4xx ou 5xx)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição à API da NovaDAX: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Status Code: {e.response.status_code}")
                print(f"Response Body: {e.response.text}")
            return {"code": "ERROR", "message": str(e), "data": None}

    # Public Endpoints
    def get_tickers(self):
        return self._send_request("GET", "/v1/market/tickers")

    def get_ticker(self, symbol):
        return self._send_request("GET", "/v1/market/ticker", params={"symbol": symbol})

    def get_depth(self, symbol, limit=10):
        return self._send_request("GET", "/v1/market/depth", params={"symbol": symbol, "limit": limit})

    def get_trades(self, symbol, limit=10):
        return self._send_request("GET", "/v1/market/trades", params={"symbol": symbol, "limit": limit})

    def get_kline(self, symbol, period, limit=10):
        return self._send_request("GET", "/v1/market/kline", params={"symbol": symbol, "period": period, "limit": limit})

    # Private Endpoints
    def get_balance(self, account_id=None):
        path = "/v1/account/getBalance"
        headers = {}
        if account_id:
            headers["X-Nova-Account-Id"] = account_id
        return self._send_request("GET", path, headers=headers)

    def create_order(self, symbol, side, order_type, size, price=None, client_order_id=None, account_id=None):
        path = "/v1/orders/create"
        data = {
            "symbol": symbol,
            "side": side, # "BUY" or "SELL"
            "type": order_type, # "LIMIT", "MARKET", "STOP_LIMIT", "STOP_MARKET"
            "size": str(size)
        }
        if price:
            data["price"] = str(price)
        if client_order_id:
            data["clientOrderId"] = client_order_id

        headers = {}
        if account_id:
            headers["X-Nova-Account-Id"] = account_id

        return self._send_request("POST", path, data=data, headers=headers)

    def cancel_order(self, order_id, account_id=None):
        path = "/v1/orders/cancel"
        data = {"orderId": str(order_id)}
        headers = {}
        if account_id:
            headers["X-Nova-Account-Id"] = account_id
        return self._send_request("POST", path, data=data, headers=headers)

    def get_order_details(self, order_id, account_id=None):
        path = "/v1/orders/get"
        params = {"orderId": str(order_id)}
        headers = {}
        if account_id:
            headers["X-Nova-Account-Id"] = account_id
        return self._send_request("GET", path, params=params, headers=headers)

    def get_order_history(self, symbol=None, start_time=None, end_time=None, limit=100, account_id=None):
        path = "/v1/orders/list"
        params = {"limit": limit}
        if symbol:
            params["symbol"] = symbol
        if start_time:
            params["startTime"] = start_time
        if end_time:
            params["endTime"] = end_time

        headers = {}
        if account_id:
            headers["X-Nova-Account-Id"] = account_id

        return self._send_request("GET", path, params=params, headers=headers)

    def get_sub_accounts(self):
        return self._send_request("GET", "/v1/account/subs")

    def get_sub_account_balance(self, sub_account_id):
        return self._send_request("GET", "/v1/account/sub-balance", params={"subAccountId": sub_account_id})


# Exemplo de uso (apenas para demonstração, as chaves devem vir de variáveis de ambiente)
if __name__ == "__main__":
    # Para testar, crie um arquivo .env na raiz do projeto com as chaves:
    # NOVADAX_ACCESS_KEY=sua_access_key
    # NOVADAX_SECRET_KEY=sua_secret_key

    try:
        api = NovaDAXAPI()

        # Exemplo: Obter tickers de mercado
        # tickers = api.get_tickers()
        # print("Tickers:", tickers)

        # Exemplo: Obter saldo da conta (requer chaves válidas e autenticação)
        # balance = api.get_balance()
        # print("Saldo:", balance)

        # Exemplo: Criar uma ordem (CUIDADO: isso pode executar uma ordem real!)
        # order = api.create_order(symbol="BTC_BRL", side="BUY", order_type="LIMIT", size=0.0001, price=100000)
        # print("Ordem criada:", order)

    except ValueError as e:
        print(f"Erro de configuração: {e}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")


