from flask import Flask, jsonify, request
from flask_cors import CORS
import threading
from config import CONFIG
from utils.logger import Logger
from utils.api_connector import APIConnector
from ias.analysis_ia import AnalysisIA
from ias.buy_ia import BuyIA
from ias.sell_ia import SellIA
from ias.stop_ia import StopIA
from ias.news_ia import NewsIA
from ias.indicators_ia import IndicatorsIA
from ias.supervisor_ia import SupervisorIA

# Inicializa Flask
app = Flask(__name__)
CORS(app)  # Permite chamadas do frontend

# Inicializa logger
logger = Logger()

# Inicializa conexão com corretoras
api_connector = APIConnector(CONFIG['api_keys'])

# Inicializa as IAs
analysis_ia = AnalysisIA(api_connector)
buy_ia = BuyIA(api_connector)
sell_ia = SellIA(api_connector)
stop_ia = StopIA(api_connector)
news_ia = NewsIA()
indicators_ia = IndicatorsIA()
supervisor_ia = SupervisorIA([analysis_ia, buy_ia, sell_ia, stop_ia, news_ia, indicators_ia])

# Função para rodar IAs em threads separadas
def run_ia(ia):
    ia.start()

# Inicia todas as IAs em threads
ia_threads = []
for ia in [analysis_ia, buy_ia, sell_ia, stop_ia, news_ia, indicators_ia, supervisor_ia]:
    t = threading.Thread(target=run_ia, args=(ia,))
    t.daemon = True
    t.start()
    ia_threads.append(t)
    logger.log(f"{ia.__class__.__name__} iniciada.")

# Rotas da API
@app.route('/status', methods=['GET'])
def status():
    """
    Retorna o status de todas as IAs e contas.
    """
    return jsonify({
        'ias': {ia.__class__.__name__: ia.get_status() for ia in [analysis_ia, buy_ia, sell_ia, stop_ia, news_ia, indicators_ia, supervisor_ia]},
        'accounts': api_connector.get_balances()
    })

@app.route('/set_stop', methods=['POST'])
def set_stop():
    """
    Configura a porcentagem de stop inteligente.
    Recebe JSON: { "stop_percent": 2 }
    """
    data = request.json
    percent = data.get('stop_percent')
    if percent is not None:
        stop_ia.set_stop_percent(percent)
        logger.log(f"Stop inteligente configurado para {percent}%")
        return jsonify({'success': True, 'stop_percent': percent})
    else:
        return jsonify({'success': False, 'error': 'stop_percent não fornecido'}), 400

@app.route('/mode', methods=['POST'])
def set_mode():
    """
    Configura o modo de operação: leve, moderado, agressivo ou automático
    Recebe JSON: { "mode": "leve" }
    """
    data = request.json
    mode = data.get('mode')
    if mode in ['leve', 'moderado', 'agressivo', 'automático']:
        supervisor_ia.set_mode(mode)
        logger.log(f"Modo de operação configurado para {mode}")
        return jsonify({'success': True, 'mode': mode})
    else:
        return jsonify({'success': False, 'error': 'Modo inválido'}), 400

# Rota teste
@app.route('/')
def index():
    return "Felps Trade backend ativo."

# Inicializa Flask
if __name__ == '__main__':
    logger.log("Servidor Flask iniciando...")
    app.run(host='0.0.0.0', port=5000, debug=False)
