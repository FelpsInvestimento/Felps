# backend/novadax_api.py
import time
import hashlib
import hmac
import requests
import json

class NovaDAXAPI:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = "https://api.novadax.com"

    # Cria assinatura para autenticação
    def _sign(self, method, path, query_string=""):
        timestamp = str(int(time.time() * 1000))
        payload = f"{timestamp}{method}{path}{query_string}"
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            payload.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return timestamp, signature

    # Faz requisição autenticada
    def _request(self, method, path, params=None):
        query_string = ""
        if params:
            query_string = "?" + "&".join([f"{k}={v}" for k, v in params.items()])

        timestamp, signature = self._sign(method, path, query_string)

        headers = {
            "X-Nova-Access-Key": self.api_key,
            "X-Nova-Timestamp": timestamp,
            "X-Nova-Signature": signature,
            "Content-Type": "application/json"
        }

        url = self.base_url + path + query_string
        response = requests.request(method, url, headers=headers, json=params if method != "GET" else None)

        if response.status_code != 200:
            raise Exception(f"Erro na requisição: {response.status_code} - {response.text}")

        return response.json()

    # Consulta saldo de todas as moedas
    def get_balance(self):
        return self._request("GET", "/v1/account/getBalance")

    # Coloca ordem de compra
    def buy(self, symbol, amount, price):
        return self._request("POST", "/v1/orders/create", {
            "symbol": symbol,
            "side": "BUY",
            "type": "LIMIT",
            "price": price,
            "quantity": amount
        })

    # Coloca ordem de venda
    def sell(self, symbol, amount, price):
        return self._request("POST", "/v1/orders/create", {
            "symbol": symbol,
            "side": "SELL",
            "type": "LIMIT",
            "price": price,
            "quantity": amount
        })

    # Cancela uma ordem
    def cancel_order(self, order_id):
        return self._request("POST", f"/v1/orders/cancel", {"id": order_id})

    # Consulta ordens abertas
    def get_open_orders(self, symbol):
        return self._request("GET", "/v1/orders/listOpen", {"symbol": symbol})

    # Consulta histórico de ordens
    def get_order_history(self, symbol):
        return self._request("GET", "/v1/orders/listHistory", {"symbol": symbol})
