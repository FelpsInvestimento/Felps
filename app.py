from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/status')
def api_status():
    return jsonify({
        "ias_operando": True,
        "conectado_novadax": True,
        "modo_operacao": "Automático",
        "lucro_total": 3287.45,
        "perda_total": 924.12,
        "saldo_disponivel": 5914.00
    })

@app.route('/api/save_keys', methods=['POST'])
def save_keys():
    data = request.json
    with open("keys.txt", "w") as f:
        f.write(data['access'] + "\n" + data['secret'])
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run()
