# backend/database.py
import sqlite3
import datetime
import os

DB_NAME = "felps_trade.db"

# Cria o banco se não existir
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Tabela de operações executadas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS trades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        conta TEXT,
        ativo TEXT,
        acao TEXT,
        quantidade REAL,
        preco REAL,
        stop_loss REAL,
        status TEXT,
        timestamp TEXT
    )
    """)

    # Tabela de relatórios resumidos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        conta TEXT,
        resumo TEXT,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()

# Função para registrar uma operação
def registrar_trade(conta, ativo, acao, quantidade, preco, stop_loss, status="EXECUTADO"):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
    INSERT INTO trades (conta, ativo, acao, quantidade, preco, stop_loss, status, timestamp)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (conta, ativo, acao, quantidade, preco, stop_loss, status, timestamp))

    conn.commit()
    conn.close()

# Função para salvar um relatório
def salvar_relatorio(conta, resumo):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
    INSERT INTO reports (conta, resumo, timestamp)
    VALUES (?, ?, ?)
    """, (conta, resumo, timestamp))

    conn.commit()
    conn.close()

# Função para consultar o histórico de trades
def listar_trades(limite=20):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM trades ORDER BY id DESC LIMIT ?", (limite,))
    rows = cursor.fetchall()
    conn.close()
    return rows

# Função para consultar relatórios
def listar_relatorios(limite=10):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reports ORDER BY id DESC LIMIT ?", (limite,))
    rows = cursor.fetchall()
    conn.close()
    return rows

# Inicializa o banco sempre que o arquivo for importado
init_db()
