from flask import Flask
from flask_cors import CORS
from app.routes import api_bp

app = Flask(__name__)
CORS(app)  # Permitir CORS para todas as rotas
app.register_blueprint(api_bp, url_prefix="/api")

@app.route("/")
def home():
    return "Bem-vindo ao FELPS TRADE Backend!"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)


