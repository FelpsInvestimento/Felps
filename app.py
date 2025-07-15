from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/salvar-config', methods=['POST'])
def salvar_config():
    dados = request.json
    print("🧠 Configurações recebidas:", dados)
    return jsonify({"mensagem": "Configurações salvas com sucesso!"})

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=5000)
