import React from "react";

function ModeSelector({ selectedMode, handleModeChange }) {
  return (
    <section className="mb-6">
      <h2 className="text-2xl font-semibold mb-2">Modos de Operação</h2>
      <div className="flex gap-4">
        {["Leve", "Moderado", "Agressivo", "Automático"].map(mode => (
          <button
            key={mode}
            className={`px-4 py-2 rounded ${selectedMode === m
