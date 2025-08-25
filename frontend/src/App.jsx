// App.jsx
import React from 'react';
import Header from './components/Header';
import StatusPanel from './components/StatusPanel';
import OperationLog from './components/OperationLog';
import AccountSelector from './components/AccountSelector';
import Balance from './components/Balance';

const App = () => {
  const handleSelectedAccounts = (contasSelecionadas) => {
    console.log('Contas selecionadas:', contasSelecionadas);
    // Aqui você pode enviar para o backend quais contas devem operar
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <div className="max-w-4xl mx-auto p-4">
        <AccountSelector onSelect={handleSelectedAccounts} />
        <Balance />
        <StatusPanel />
        <OperationLog />
      </div>
    </div>
  );
};

export default App;
