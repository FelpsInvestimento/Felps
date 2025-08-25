// OperationLog.jsx
import React, { useState, useEffect } from 'react';

const OperationLog = () => {
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    // Simulação de fetch do backend para logs de operações
    const fetchLogs = () => {
      fetch('/api/logs')  // Endpoint do backend que retorna os logs
        .then(res => res.json())
        .then(data => setLogs(data))
        .catch(() => console.error('Erro ao buscar logs'));
    };

    fetchLogs();
    const interval = setInterval(fetchLogs, 5000); // Atualiza a cada 5s
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="bg-white p-4 rounded shadow-md mt-4 h-64 overflow-y-auto">
      <h2 className="text-xl font-semibold mb-2">Logs de Operações</h2>
      <ul>
        {logs.map((log, index) => (
          <li key={index} className="mb-1">
            [{log.horario}] {log.mensagem}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default OperationLog;
