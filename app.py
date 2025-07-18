from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# Rota principal
@app.route("/")
def index():
    return render_template("index.html")

# Exemplo de rota para simulação (pode personalizar)
@app.route("/api/simulacao", methods=["POST"])
def simulacao():
    data = request.get_json()
    resposta = {
        "status": "sucesso",
        "mensagem": "Simulação processada",
        "dadosRecebidos": data
    }
    return jsonify(resposta)

# Isso permite que funcione corretamente no Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render define a porta como variável de ambiente
    app.run(host="0.0.0.0", port=port)        # Flask roda publicamente no host 0.0.0.0
