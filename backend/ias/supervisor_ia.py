import time
from utils.logger import Logger

class SupervisorIA:
    def __init__(self, ias, interval=10):
        """
        Inicializa a IA supervisora.
        ias: dicionário com referências para todas as IAs do sistema
        interval: tempo em segundos entre verificações
        """
        self.ias = ias  # Ex: {"analysis": analysis_ia, "buy": buy_ia, ...}
        self.logger = Logger()
        self.interval = interval
        self.status = "Iniciando"

    def start(self):
        """
        Inicia o monitoramento contínuo das IAs.
        """
        self.logger.log("SupervisorIA iniciada")
        self.status = "Rodando"
        while True:
            try:
                self.check_ias()
            except Exception as e:
                self.logger.log(f"ERRO SupervisorIA: {e}")
            time.sleep(self.interval)

    def check_ias(self):
        """
        Verifica status de cada IA e registra problemas.
        """
        for name, ia in self.ias.items():
            try:
                status = ia.get_status()
                if status.get("status") != "Rodando":
                    self.logger.log(f"SupervisorIA: {name} não está rodando corretamente: {status}")
                else:
                    self.logger.log(f"SupervisorIA: {name} OK")
            except Exception as e:
                self.logger.log(f"SupervisorIA: falha ao acessar {name}: {e}")

    def get_status(self):
        """
        Retorna status geral de todas as IAs.
        """
        status_dict = {}
        for name, ia in self.ias.items():
            try:
                status_dict[name] = ia.get_status()
            except:
                status_dict[name] = {"status": "Erro ao acessar"}
        return {"status": self.status, "ias_status": status_dict}
