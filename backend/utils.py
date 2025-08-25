# backend/utils.py
import datetime
import json
import os

# Função para registrar logs em arquivo
def log_message(message, log_file="logs/trade_logs.txt"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_message = f"[{timestamp}] {message}"
    print(full_message)

    # Cria a pasta de logs se não existir
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(full_message + "\n")

# Função para salvar relatórios de operações
def save_report(data, report_file="logs/report.json"):
    os.makedirs(os.path.dirname(report_file), exist_ok=True)

    if not os.path.exists(report_file):
        with open(report_file, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4)

    with open(report_file, "r+", encoding="utf-8") as f:
        reports = json.load(f)
        reports.append(data)
        f.seek(0)
        json.dump(reports, f, indent=4)

# Função para formatar valores em moeda
def format_currency(value, currency="BRL"):
    return f"{value:,.2f} {currency}"

# Função para exibir saldo em tempo real formatado
def show_balance(balance_dict):
    print("=== SALDO ATUAL ===")
    for coin, amount in balance_dict.items():
        print(f"{coin}: {amount:,.6f}")

# Função de motivação (vai aparecer no console também)
def motivational_message():
    return "🚀 EU QUERO, EU POSSO, EU CONSIGO. JÁ DEU CERTO! 🚀"
