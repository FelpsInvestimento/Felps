// Balance.jsx
import React, { useState, useEffect } from 'react';

const Balance = () => {
  const [saldo, setSaldo] = useState(0);

  useEffect(() => {
    const fetchBalance = () => {
      fetch('/api/balance')  // Endpoint do backend que retorna saldo em tempo real
        .then(res => res.json())
        .then(data => setSaldo(data.saldo))
        .catch(() => setSaldo('Erro ao obter saldo'));
    };

    fetchBalance();
    const interval = setInterval(fetchBalance, 5000); // Atualiza a cada 5 segundos
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="bg-white p-4 rounded shadow-md mt-4">
      <h2 className="text-xl font-semibold mb-2">Saldo Disponível</h2>
      <p className="text-lg font-bold">{typeof saldo === 'number' ? `R$ ${saldo.toFixed(2)}` : saldo}</p>
    </div>
  );
};

export default Balance;
