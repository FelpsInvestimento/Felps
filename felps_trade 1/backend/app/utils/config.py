import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    NOVADAX_ACCESS_KEY = os.getenv('NOVADAX_ACCESS_KEY')
    NOVADAX_SECRET_KEY = os.getenv('NOVADAX_SECRET_KEY')
    # Adicione outras configurações aqui, se necessário


