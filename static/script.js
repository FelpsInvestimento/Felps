function toggleVisibility(id) {
  const field = document.getElementById(id);
  field.type = field.type === "password" ? "text" : "password";
}
// ... continuação anterior ...
function mostrarRelatoriosAoVivo() {
  fetch('/relatorios_ao_vivo')
    .then(res => res.json())
    .then(data => {
      const relatoriosDiv = document.getElementById('relatorios-ao-vivo');
      relatoriosDiv.innerHTML = "";
      data.forEach(item => {
        const bloco = document.createElement('div');
        bloco.className = "relatorio-item";
        bloco.innerHTML = `
          <strong>${item.ia}</strong> <br>
          Ativo: ${item.ativo}<br>
          Ação: ${item.acao}<br>
          Lucro: R$ ${item.lucro}<br>
          Confiança: ${item.confianca}%
        `;
        relatoriosDiv.appendChild(bloco);
      });
    });
}
setInterval(mostrarRelatoriosAoVivo, 4000);

