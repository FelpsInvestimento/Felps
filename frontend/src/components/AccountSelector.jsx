// AccountSelector.jsx
import React, { useState, useEffect } from 'react';

const AccountSelector = ({ onSelect }) => {
  const [contas, setContas] = useState([
    { id: 1, nome: 'Conta 1', selecionada: true },
    { id: 2, nome: 'Conta 2', selecionada: true },
    { id: 3, nome: 'Conta 3', selecionada: true },
    { id: 4, nome: 'Conta 4', selecionada: false },
    { id: 5, nome: 'Conta 5', selecionada: false },
    { id: 6, nome: 'Conta 6', selecionada: false },
    { id: 7, nome: 'Conta 7', selecionada: false },
    { id: 8, nome: 'Conta 8', selecionada: false },
    { id: 9, nome: 'Conta 9', selecionada: false },
    { id: 10, nome: 'Conta 10', selecionada: false },
  ]);

  const toggleConta = (id) => {
    const novasContas = contas.map(conta =>
      conta.id === id ? { ...conta, selecionada: !conta.selecionada } : conta
    );
    setContas(novasContas);
    if (onSelect) {
      onSelect(novasContas.filter(c => c.selecionada));
    }
  };

  useEffect(() => {
    if (onSelect) {
      onSelect(contas.filter(c => c.selecionada));
    }
  }, []);

  return (
    <div className="bg-gray-100 p-4 rounded shadow-md mt-4">
      <h2 className="text-xl font-semibold mb-2">Selecionar Contas</h2>
      <div className="grid grid-cols-2 gap-2">
        {contas.map(conta => (
          <button
            key={conta.id}
            className={`p-2 rounded ${conta.selecionada ? 'bg-green-500 text-white' : 'bg-gray-300 text-black'}`}
            onClick={() => toggleConta(conta.id)}
          >
            {conta.nome}
          </button>
        ))}
      </div>
    </div>
  );
};

export default AccountSelector;
