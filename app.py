from flask import Flask, render_template, request
import threading
import time

app = Flask(__name__)

# Simula o status da API e inicializa variáveis globais
api_status = {"ok": False, "key": "", "secret": ""}
modo_ativo = "Auto"
valor_entrada = 100

# Simulação de 200 IAs
class InteligenciaArtificial:
    def __init__(self, id):
        self.id = id
        self.ativo = True

    def operar(self):
        while self.ativo:
            if api_status["ok"]:
                print(f"IA {self.id} operando com {modo_ativo}...")
            time.sleep(10)  # Simula tempo de decisão e operação

ias = [InteligenciaArtificial(i+1) for i in range(200)]

# Thread para iniciar as IAs
thread_pool = []
def iniciar_operacoes():
    for ia in ias:
        t = threading.Thread(target=ia.operar)
        t.start()
        thread_pool.append(t)

@app.route("/", methods=["GET", "POST"])
def index():
    global api_status, modo_ativo, valor_entrada

    if request.method == "POST":
        api_status["key"] = request.form.get("api_key")
        api_status["secret"] = request.form.get("secret_key")
        modo_ativo = request.form.get("modo")
        valor_entrada = float(request.form.get("valor_entrada") or 0)

        if api_status["key"] and api_status["secret"]:
            api_status["ok"] = True
            print("✅ API conectada com sucesso.")

        return render_template("index.html")

    return render_template("index.html")

if __name__ == "__main__":
    iniciar_operacoes()
    app.run(host="0.0.0.0", port=5000)

