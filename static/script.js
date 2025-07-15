
function toggleVisibility(id) {
  const input = document.getElementById(id);
  input.type = input.type === "password" ? "text" : "password";
}

function salvarConfiguracoes() {
  const dados = {
    conta: document.getElementById("conta").value,
    accessKey: document.getElementById("accessKey").value,
    secretKey: document.getElementById("secretKey").value,
    valor: document.getElementById("valor").value,
    modo: document.querySelector('input[name="modo"]:checked')?.value
  };

  fetch("/salvar-config", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(dados)
  })
    .then(res => res.json())
    .then(res => {
      alert("✅ Configurações salvas com sucesso!");
      console.log(res);
    })
    .catch(err => {
      alert("Erro ao salvar configurações.");
      console.error(err);
    });
}

window.onload = () => {
  const container = document.getElementById("ias");
  for (let i = 1; i <= 200; i++) {
    const ia = document.createElement("div");
    ia.className = "ia";
    ia.innerText = `IA ${i}`;
    container.appendChild(ia);
  }
};
