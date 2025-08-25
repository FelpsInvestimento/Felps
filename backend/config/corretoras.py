# corretoras.py

class Corretora:
    def __init__(self, nome, api_class):
        self.nome = nome
        self.api_class = api_class

# Aqui você pode importar o módulo da API de cada corretora
from novadax_api import NovadaxAPI

# Lista de corretoras disponíveis
corretoras_disponiveis = [
    Corretora(nome="NovaDAX", api_class=NovadaxAPI)
]

def listar_corretoras():
    return [c.nome for c in corretoras_disponiveis]
