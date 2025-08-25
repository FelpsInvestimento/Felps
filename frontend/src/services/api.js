import axios from "axios";

const API_BASE = "http://localhost:5000"; // Ajuste caso o backend esteja em outro endereço

// Busca status das IAs
export const getIasStatus = async () => {
  try {
    const res = await axios.get(`${API_BASE}/status`);
    return res.data.ias_status;
  } catch (err) {
    console.error("Erro ao buscar status das IAs:", err);
    return {};
  }
};

// Busca saldos das contas
export const getBalances = async () => {
  try {
    const res = await axios.get(`${API_BASE}/balances`);
    return res.data;
  } catch (err) {
    console.error("Erro ao buscar saldos:", err);
    return {};
  }
};

// Define o modo de operação
export const setMode = async (mode) => {
  try {
    await axios.post(`${API_BASE}/set_mode`, { mode });
  } catch (err) {
    console.error("Erro ao definir modo:", err);
  }
};

// Define o percentual de stop loss
export const setStopPercent = async (percent) => {
  try {
    await axios.post(`${API_BASE}/set_stop_percent`, { percent });
  } catch (err) {
    console.error("Erro ao definir stop percent:", err);
  }
};
