import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [iasStatus, setIasStatus] = useState({});
  const [selectedMode, setSelectedMode] = useState("Automático");
  const [stopPercent, setStopPercent] = useState(2);
  const [balances, setBalances] = useState({});
  const [accounts, setAccounts] = useState(["Conta 1", "Conta 2", "Conta 3"]);

  useEffect(() => {
    const interval = setInterval(() => {
      fetchStatus();
      fetchBalances();
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  const fetchStatus = async () => {
    try {
      const res = await axios.get("http://localhost:5000/status");
      setIasStatus(res.data.ias_status);
    } catch (err) {
      console.error("Erro ao buscar status:", err);
    }
  };

  const fetchBalances = async () => {
    try {
      const res = await axios.get("http://localhost:5000/balances");
      setBalances(res.data);
    } catch (err) {
      console.error("Erro ao buscar saldos:", err);
    }
  };

  const handleModeChange = (mode) => {
    setSelectedMode(mode);
    axios.post("http://localhost:5000/set_mode", { mode });
  };

  const handleStopChange = (e) => {
    const value = parseFloat(e.target.value);
    setStopPercent(value);
    axios.post("http://localhost:5000/set_stop_percent", { percent: value });
  };

  return (
    <div className="min-h-screen p-6 bg-gray-100">
      <header className="text-center mb-6">
        <h1 className="text-4xl font-bold text-green-700">Felps Trade</h1>
        <p className="text-xl text-gray-700 mt-2">
          EU QUERO, EU POSSO E EU CONSIGO. JÁ DEU CERTO.
        </p>
      </header>

      <section className="mb-6">
        <h2 className="text-2xl font-semibold mb-2">Modos de Operação</h2>
        <div className="flex gap-4">
          {["Leve", "Moderado", "Agressivo", "Automático"].map(mode => (
            <button
              key={mode}
              className={`px-4 py-2 rounded ${selectedMode === mode ? 'bg-green-700 text-white' : 'bg-gray-300'}`}
              onClick={() => handleModeChange(mode)}
            >
              {mode}
            </button>
          ))}
        </div>
      </section>

      <section className="mb-6">
        <h2 className="text-2xl font-semibold mb-2">Stop Loss Inteligente (%)</h2>
        <input
          type="number"
          value={stopPercent}
          onChange={handleStopChange}
          className="border p-2 rounded w-20"
          min="0.1"
          step="0.1"
        />
      </section>

      <section className="mb-6">
        <h2 className="text-2xl font-semibold mb-2">Status das IAs</h2>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
          {Object.entries(iasStatus).map(([name, status]) => (
            <div key={name} className="p-4 bg-white rounded shadow">
              <h3 className="font-bold">{name}</h3>
              <p>Status: {status.status}</p>
            </div>
          ))}
        </div>
      </section>

      <section>
        <h2 className="text-2xl font-semibold mb-2">Saldos das Contas</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {accounts.map(acc => (
            <div key={acc} className="p-4 bg-white rounded shadow">
              <h3 className="font-bold">{acc}</h3>
              <p>USDT: {balances[acc]?.USDT ?? 0}</p>
              <p>BTC: {balances[acc]?.BTC ?? 0}</p>
              <p>ETH: {balances[acc]?.ETH ?? 0}</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}

export default App;
