import os
import json
from datetime import datetime

RELATORIO_PATH = "relatorios/"
os.makedirs(RELATORIO_PATH, exist_ok=True)

def registrar_operacao(ia_id, ativo, tipo, valor, resultado, modo, simulada=False):
    data = datetime.now().strftime("%Y-%m-%d")
    hora = datetime.now().strftime("%H:%M:%S")

    registro = {
        "ia": ia_id,
        "ativo": ativo,
        "tipo": tipo,
        "valor": valor,
        "resultado": resultado,
        "hora": hora,
        "modo": modo,
        "simulada": simulada
    }

    nome_arquivo = f"{RELATORIO_PATH}{data}.json"

    if os.path.exists(nome_arquivo):
        with open(nome_arquivo, "r") as f:
            registros = json.load(f)
    else:
        registros = []

    registros.append(registro)

    with open(nome_arquivo, "w") as f:
        json.dump(registros, f, indent=2)

def obter_relatorio(data=None):
    if data is None:
        data = datetime.now().strftime("%Y-%m-%d")
    nome_arquivo = f"{RELATORIO_PATH}{data}.json"
    
    if os.path.exists(nome_arquivo):
        with open(nome_arquivo, "r") as f:
            return json.load(f)
    return []
