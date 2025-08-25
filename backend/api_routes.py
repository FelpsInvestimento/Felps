# backend/api_routes.py
from flask import Blueprint, jsonify, request
import json
from novadax_api import NovaDAXAPI

api_bp = Blueprint("api", __name__)

# Instância da API (config inicial)
api = NovaDAXAPI(api_key="SUA_API_KEY", api_secret="SEU_API_SECRET")

# Estado inicial do robô
estado_robo = {
    "ia_ativa": True,
    "modo": "Automático",
    "conta_selecionada": 1,
    "relatorios": []
}

# Testa se as IAs estão funcionando
@api_bp.route("/status", methods=["GET"])
def status_robo():
    return jsonify({
        "mensagem": "IAs rodando normalmente",
        "ia_ativa": estado_robo["ia_ativa"],
        "modo": estado_robo["modo"],
        "conta": estado_robo["conta_selecionada"]
    })

# Retorna saldo da conta
@api_bp.route("/saldo", methods=["GET"])
def saldo():
    try:
        saldo_data = api.get_balance()
        return jsonify(saldo_data)
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# Muda o modo de operação (Leve, Moderado, Agressivo, Automático)
@api_bp.route("/modo", methods=["POST"])
def mudar_modo():
    data = request.json
    if "modo" not in data:
        return jsonify({"erro": "Modo não informado"}), 400
    estado_robo["modo"] = data["modo"]
    return jsonify({"mensagem": f"Modo alterado para {data['modo']}"})

# Seleciona conta (1 a 10)
@api_bp.route("/conta", methods=["POST"])
def mudar_conta():
    data = request.json
    conta = data.get("conta")
    if not conta or not (1 <= conta <= 10):
        return jsonify({"erro": "Número de conta inválido"}), 400
    estado_robo["conta_selecionada"] = conta
    return jsonify({"mensagem": f"Conta alterada para Conta {conta}"})

# Retorna relatório de operações
@api_bp.route("/relatorios", methods=["GET"])
def relatorios():
    return jsonify(estado_robo["relatorios"])
