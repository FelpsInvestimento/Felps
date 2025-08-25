import React from "react";

function StopConfig({ stopPercent, handleStopChange }) {
  return (
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
  );
}

export default StopConfig;
