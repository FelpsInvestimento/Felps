import React from "react";

function Dashboard({ iasStatus, balances, accounts, selectedMode, setSelectedMode, stopPercent, setStopPercent, handleModeChange, handleStopChange }) {
  return (
    <main>
      {/* Modos de Operação */}
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

      {/* Stop Loss Inteligente */}
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

      {/* Status das IAs */}
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

      {/* Saldos das Contas */}
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
    </main>
  );
}

export default Dashboard;
