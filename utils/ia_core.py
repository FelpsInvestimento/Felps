import threading
import time
from core.analisador import analisar_ativo
from core.executor import executar_ordem
from core.gestao import verificar_risco
from core.relatorio import registrar_acao
from supervisora import supervisora_log
from database.cache import atualizar_cache

class IA:
    def __init__(self, nome, estrategia):
        self.nome = nome
        self.estrategia = estrategia
        self.ativo = None
        self.operando = False
        self.confiança = 0.0
        self.resultado = None

    def iniciar(self, ativo):
        self.ativo = ativo
        self.operando = True
        threading.Thread(target=self.operar).start()

    def operar(self):
        while self.operando:
            analise = analisar_ativo(self.ativo, self.estrategia)
            if not verificar_risco(analise):
                self.confiança = 0.0
                self.resultado = "Risco alto"
                supervisora_log(f"{self.nome}: operação cancelada por risco")
                break

            resultado = executar_ordem(self.ativo, analise)
            self.resultado = resultado["resumo"]
            self.confiança = resultado["confianca"]

            registrar_acao(self.nome, self.ativo, self.resultado, self.confiança)
            atualizar_cache(self.nome, self.ativo, self.resultado, self.confiança)

            if resultado["finalizado"]:
                break

            time.sleep(1)

    def parar(self):
        self.operando = False
