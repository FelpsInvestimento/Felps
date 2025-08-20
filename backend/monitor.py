# backend/monitor.py

import time
import logging
from database import salvar_operacao
from novadax_api import NovaDAXAPI
from config import CONTAS, ROBO_NOME
from utils import gerar_timestamp

# Configuração de logs
logging.basicConfig(
    filename="monitor.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

class Monitor:
    def __init__(self):
        self.contas = CONTAS
        self.apis = {conta: NovaDAXAPI(keys["API_KEY"], keys["SECRET_KEY"]) for conta, keys in self.contas.items()}

    def verificar_api(self):
        """Verifica se a API da NovaDAX está funcionando para todas as contas"""
        resultados = {}
        for conta, api in self.apis.items():
            try:
                saldo = api.get_balance()
                if saldo:
                    resultados[conta] = "OK"
                else:
                    resultados[conta] = "FALHA"
            except Exception as e:
                resultados[conta] = f"ERRO: {e}"
        return resultados

    def verificar_banco(self):
        """Testa se o banco de dados responde"""
        try:
            salvar_operacao("sistema", "teste", 0, "teste", "sucesso")
            return "Banco OK"
        except Exception as e:
            return f"Banco ERRO: {e}"

    def rodar_monitoramento(self, intervalo=60):
        """Roda o monitoramento contínuo"""
        print(f"🔍 Iniciando monitoramento do {ROBO_NOME}...")
        while True:
            # Verificar APIs
            status_api = self.verificar_api()
            # Verificar Banco
            status_banco = self.verificar_banco()

            # Registrar logs
            logging.info(f"Status API: {status_api}")
            logging.info(f"Status Banco: {status_banco}")

            # Mostrar no console
            print(f"[{gerar_timestamp()}] Status APIs: {status_api} | Banco: {status_banco}")

            # Aguardar antes da próxima checagem
            time.sleep(intervalo)


if __name__ == "__main__":
    monitor = Monitor()
    monitor.rodar_monitoramento(intervalo=60)  # verifica a cada 60 segundos
