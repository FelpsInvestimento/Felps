from flask import Blueprint, request, jsonify
from app.services.trade_manager import TradeManager

# Configuração de exemplo para múltiplas contas
# Em um ambiente real, isso viria de um banco de dados ou arquivo de configuração seguro
# As chaves de API devem ser carregadas de forma segura (e.g., de variáveis de ambiente)
# Para este exemplo, estamos usando as chaves fornecidas diretamente (APENAS PARA TESTE)
# Em produção, use Config.NOVADAX_ACCESS_KEY e Config.NOVADAX_SECRET_KEY

# ATENÇÃO: As chaves de API abaixo são as fornecidas pelo usuário e devem ser tratadas com EXTREMA CAUTELA.
# Em um ambiente de produção, elas DEVERIAM ser carregadas de variáveis de ambiente seguras
# e NUNCA hardcoded no código-fonte.
accounts_config = {
    "CONTA_1": {
        "access_key": "fb17caa1-00a5-45ad-800f-31dcff935376",
        "secret_key": "IDqP2LKyivmnBprsRQ8qzLt6oQPQNWGo"
    },
    # Adicione mais contas aqui conforme necessário, seguindo o mesmo formato
    # "CONTA_2": {
    #     "access_key": os.getenv("NOVADAX_ACCESS_KEY_2"),
    #     "secret_key": os.getenv("NOVADAX_SECRET_KEY_2")
    # },
}

trade_manager = TradeManager(accounts_config, initial_settings={})
api_bp = Blueprint("api", __name__)

@api_bp.route("/status", methods=["GET"])
def get_status():
    status = trade_manager.get_robot_status()
    return jsonify(status)

@api_bp.route("/start", methods=["POST"])
def start_robot():
    trade_manager.start_robot()
    return jsonify({"message": "Robô iniciado com sucesso!"})

@api_bp.route("/stop", methods=["POST"])
def stop_robot():
    trade_manager.stop_robot()
    return jsonify({"message": "Robô parado com sucesso!"})

@api_bp.route("/balance", methods=["GET"])
def get_balance():
    balances = trade_manager.get_all_balances()
    return jsonify(balances)

@api_bp.route("/mode", methods=["POST"])
def set_mode():
    data = request.get_json()
    mode = data.get("mode")
    if mode:
        trade_manager.set_trading_mode(mode.upper())
        return jsonify({"message": f"Modo de negociação alterado para {mode.upper()}"})
    return jsonify({"error": "Modo não fornecido."}), 400

@api_bp.route("/mode", methods=["GET"])
def get_mode():
    mode = trade_manager.get_trading_mode()
    return jsonify({"mode": mode})

@api_bp.route("/log", methods=["GET"])
def get_log():
    log = trade_manager.get_operations_log()
    return jsonify(log)

@api_bp.route("/ias_status", methods=["GET"])
def get_ias_status():
    status = trade_manager.check_ias_functioning()
    return jsonify(status)




@api_bp.route("/settings", methods=["POST"])
def update_settings():
    data = request.get_json()
    if data:
        trade_manager.update_global_settings(data)
        return jsonify({"message": "Configurações atualizadas com sucesso!"})
    return jsonify({"error": "Nenhuma configuração fornecida."}), 400


