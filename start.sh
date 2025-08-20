#!/bin/bash

# start.sh - Script para rodar backend e frontend localmente

echo "Iniciando Felps Trade..."

# Rodar backend Flask
echo "Iniciando backend..."
cd backend
export FLASK_APP=app.py
export FLASK_ENV=development
flask run &  # Executa em segundo plano

# Rodar frontend React
echo "Iniciando frontend..."
cd ../frontend
npm install  # Instala dependências (somente na primeira vez)
npm start &  # Executa em segundo plano

echo "Felps Trade rodando! Backend: http://127.0.0.1:5000 | Frontend: http://localhost:3000"

# Espera até que o usuário pressione CTRL+C
wait
