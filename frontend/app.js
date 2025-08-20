// frontend/app.js

import React, { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";

// Componente principal
function App() {
  const [saldo, setSaldo] = useState({});
  const [statusIA, setStatusIA] = useState("Carregando...");
  const [relatorio, setRelatorio] = useState([]);
  const [modo, setModo] = useState("Automático");

  // Função para buscar saldo do backend
  const fetchSaldo = async () => {
    try {
      const response = await fetch("http://localhost:8000/saldo");
      const data = await response.json();
      setSaldo(data);
    } catch (error) {
      console.error("Erro ao buscar saldo:", error);
    }
  };

  // Função para buscar status das IAs
  const fetchStatusIA = async () => {
    try {
      const response = await fetch("http://localhost:8000/status");
      const data = await response.json();
      setStatusIA(data.status);
    } catch (error) {
      console.error("Erro ao buscar status IA:", error);
    }
  };

  // Função para buscar relatório de operações
  const fetchRelatorio = async () => {
    try {
      const response = await fetch("http://localhost:8000/relatorio");
      const data = await response.json();
      setRelatorio(data);
    } catch (error) {
      console.error("Erro ao buscar relatório:", error);
    }
  };

  // Atualiza automaticamente a cada 5 segundos
  useEffect(() => {
    fetchSaldo();
    fetchStatusIA();
    fetchRelatorio();
    const interval = setInterval(() => {
      fetchSaldo();
      fetchStatusIA();
      fetchRelatorio();
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>💹 FELPS TRADE</h1>
      <p style={styles.motivacao}>EU QUERO, EU POSSO E EU CONSIGO. JÁ DEU CERTO.</p>

      {/* Escolha de modo */}
      <div style={styles.modoBox}>
        <label>Modo de operação:</label>
        <select value={modo} onChange={(e) => setModo(e.target.value)} style={styles.select}>
          <option value="Leve">Leve</option>
          <option value="Moderado">Moderado</option>
          <option value="Agressivo">Agressivo</option>
          <option value="Automático">Automático</option>
        </select>
      </div>

      {/* Saldo */}
      <h2>Saldo das contas</h2>
      <pre style={styles.box}>{JSON.stringify(saldo, null, 2)}</pre>

      {/* Status das IAs */}
      <h2>Status das IAs</h2>
      <p style={styles.status}>{statusIA}</p>

      {/* Relatório */}
      <h2>Relatório de Operações</h2>
      <ul style={styles.lista}>
        {relatorio.length > 0 ? (
          relatorio.map((op, index) => (
            <li key={index}>
              {op.data} - {op.ativo} - {op.tipo} - {op.resultado}
            </li>
          ))
        ) : (
          <p>Nenhuma operação registrada.</p>
        )}
      </ul>
    </div>
  );
}

// Estilos inline
const styles = {
  container: {
    fontFamily: "Arial, sans-serif",
    padding: "20px",
    maxWidth: "800px",
    margin: "auto",
    backgroundColor: "#f9f9f9",
    borderRadius: "12px",
    boxShadow: "0px 4px 12px rgba(0,0,0,0.1)",
  },
  title: {
    textAlign: "center",
    color: "#2c3e50",
  },
  motivacao: {
    textAlign: "center",
    fontSize: "18px",
    color: "#27ae60",
    marginBottom: "20px",
  },
  modoBox: {
    marginBottom: "20px",
  },
  select: {
    marginLeft: "10px",
    padding: "5px",
  },
  box: {
    background: "#fff",
    padding: "10px",
    borderRadius: "8px",
    boxShadow: "inset 0px 2px 6px rgba(0,0,0,0.1)",
    fontSize: "14px",
    whiteSpace: "pre-wrap",
  },
  status: {
    fontWeight: "bold",
    color: "#2980b9",
  },
  lista: {
    background: "#fff",
    padding: "10px",
    borderRadius: "8px",
    listStyle: "none",
    boxShadow: "inset 0px 2px 6px rgba(0,0,0,0.1)",
  },
};

// Renderizar na página
const container = document.getElementById("root");
const root = createRoot(container);
root.render(<App />);
