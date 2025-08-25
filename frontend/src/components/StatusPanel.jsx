// StatusPanel.jsx
import React, { useState, useEffect } from 'react';

const StatusPanel = () => {
  const [iasStatus, setIasStatus] = useState([]);
  const [conexaoStatus, setConexaoStatus] = useState('Conectando...');

  useEffect(() => {
    // Simulação de fetch do backend para status das IAs
    const fetchStatus = () => {
      fetch('/api/status')  // Endpoint do backend que retorna status das IAs
        .then(res => res.json())
        .then(data => {
          setIasStatus(data.ias);
          setConexaoStatus(data.conexao);
        })
        .catch(() => setConexaoStatus('Erro na conexão'));
    };

    fetchStatus();
    const interval = setInterval(fetchStatus, 5000); // Atualiza a cada 5s
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="bg-gray-100 p-4 rounded shadow-md mt-4">
      <h2 className="text-xl font-semibold mb-2">Status do Robô</h2>
      <p className="mb-2">Conexão com a corretora: <span className="font-bold">{conexaoStatus}</span></p>
      <ul>
        {iasStatus.map((ia, index) => (
          <li key={index} className="mb-1">
            <span className="font-bold">{ia.nome}</span>: {ia.status}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default StatusPanel;
