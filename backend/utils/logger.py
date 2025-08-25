import datetime
import os
from config import CONFIG

class Logger:
    def __init__(self, log_file=None):
        """
        Inicializa o logger.
        Se não for informado log_file, usa o definido em CONFIG.
        """
        self.log_file = log_file or CONFIG.get('log_file', 'felps_trade.log')
        # Cria o arquivo se não existir
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w') as f:
                f.write(f"=== Início do log Felps Trade {datetime.datetime.now()} ===\n")

    def log(self, message):
        """
        Registra uma mensagem com timestamp.
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        full_message = f"[{timestamp}] {message}"
        # Exibe no console
        print(full_message)
        # Escreve no arquivo
        with open(self.log_file, 'a') as f:
            f.write(full_message + "\n")

    def log_error(self, message):
        """
        Registra mensagens de erro.
        """
        self.log(f"ERRO: {message}")
