# backend/main.py
from flask import Flask
from flask_cors import CORS
import threading
import time
from api_routes import api_bp
from trade_engine import iniciar_trade

app = Flask(__name__)
CORS(app)  # Permite o frontend acessar o backend

# Registra as rotas da API
app.register_blueprint(api_bp)

# Função para rodar o motor de trade em thread separada
def iniciar_motor_trade():
    while True:
        try:
            iniciar_trade()
        except Exception as e:
            print(f"[ERRO NO MOTOR DE TRADE] {e}")
        time.sleep(5)  # Espera 5 segundos antes de repetir

if __name__ == "__main__":
    # Inicia o motor de trade em segundo plano
    thread_trade = threading.Thread(target=iniciar_motor_trade, daemon=True)
    thread_trade.start()

    # Inicia o servidor Flask
    app.run(host="0.0.0.0", port=5000)
