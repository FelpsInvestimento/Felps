import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "./index.css"; // Importa os estilos globais

// Cria a raiz do React e renderiza o App
const root = ReactDOM.createRoot(document.getElementById("root"));

root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
