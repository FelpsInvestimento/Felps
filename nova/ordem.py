import requests
import hmac
import hashlib
import time
import json
from config.config import ACCESS_KEY, SECRET_KEY
from core.relatorio import registrar_operacao

BASE_URL = "https://api.novadax.com"

def _assinatura(metodo, path, timestamp, body=""):
    texto = f"{timestamp}{metodo}{path}{body}"
    return hmac.new(SECRET_KEY.encode(), texto.encode(), hashlib.sha256).hexdigest()

def _headers(metodo, path, body=""):
    timestamp = str(int(time.time() * 1000))
    assinatura = _assinatura(metodo, path, timestamp, body)
    return {
        "X-Nova-Access-Key": ACCESS_KEY,
        "X-Nova-Signature": assinatura,
        "X-Nova-Timestamp": timestamp,
        "Content-Type": "application/json"
    }

def enviar_ordem(ia_id, simbolo, tipo_ordem, quantidade, preco=None, modo="auto", simulada=False):
    """
    tipo_ordem: 'buy' ou 'sell'
    """
    path = "/v1/orders"
    url = BASE_URL + path
    metodo = "POST"

    body = {
        "symbol": simbolo,
        "side": tipo_ordem,
        "type": "market" if preco is None else "limit",
        "quantity": str(quantidade)
    }

    if preco is not None:
        body["price"] = str(preco)

    body_str = json.dumps(body)

    if simulada:
        print(f"[SIMULADA] Ordem {tipo_ordem.upper()} de {quantidade} {simbolo} (IA {ia_id})")
        registrar_operacao(ia_id, simbolo, tipo_ordem, quantidade, "simulada", modo, simulada=True)
        return {"status": "ok", "simulada": True}

    try:
        headers = _headers(metodo, path, body_str)
        resposta = requests.post(url, data=body_str, headers=headers)

        if resposta.status_code == 200:
            data = resposta.json()
            registrar_operacao(ia_id, simbolo, tipo_ordem, quantidade, "realizada", modo)
            return {"status": "ok", "resposta": data}
        else:
            registrar_operacao(ia_id, simbolo, tipo_ordem, quantidade, "erro", modo)
            return {"status": "erro", "detalhes": resposta.text}

    except Exception as e:
        registrar_operacao(ia_id, simbolo, tipo_ordem, quantidade, "falha", modo)
        return {"status": "falha", "erro": str(e)}
