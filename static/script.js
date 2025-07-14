function getContaSelecionada() {
  return document.getElementById("conta").value;
}

function salvarDados() {
  const conta = getContaSelecionada();
  const api = document.getElementById("api").value;
  const valor = document.getElementById("valor").value;
  const modo = localStorage.getItem(`modo_${conta}`) || "leve";

  localStorage.setItem(`api_${conta}`, api);
  localStorage.setItem(`valor_${conta}`, valor);
  localStorage.setItem(`modo_${conta}`, modo);
}

function carregarDados() {
  const conta = getContaSelecionada();
  document.getElementById("api").value = localStorage.getItem(`api_${conta}`) || "";
  document.getElementById("valor").value = localStorage.getItem(`valor_${conta}`) || "";
  const modo = localStorage.getItem(`modo_${conta}`) || "leve";
  atualizarModoVisual(modo);
}

function trocarConta() {
  carregarDados();
}

function selecionarModo(modo) {
  const conta = getContaSelecionada();
  localStorage.setItem(`modo_${conta}`, modo);
  atualizarModoVisual(modo);
  salvarDados();
}

function atualizarModoVisual(modo) {
  const botoes = document.querySelectorAll(".botoes-modo button");
  botoes.forEach(btn => {
    btn.style.border = btn.textContent.toLowerCase() === modo ? "2px solid #58a6ff" : "none";
  });
}

function gerarIAs() {
  const grid = document.getElementById("ia-grid");
  for (let i = 1; i <= 200; i++) {
    const card = document.createElement("div");
    card.className = "ia-card";
    card.textContent = `IA ${i}`;
    grid.appendChild(card);
  }
}

document.addEventListener("DOMContentLoaded", () => {
  carregarDados();
  gerarIAs();
});
