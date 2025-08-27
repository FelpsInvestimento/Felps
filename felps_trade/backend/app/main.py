from flask import Flask, jsonify

app = Flask(__name__)

# Rota principal para evitar erro 404
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "API do Felps Trade funcionando!"}), 200

# Rota de health check
@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(debug=True)



