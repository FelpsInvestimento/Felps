// Mostrar/ocultar campo de senha
function toggleVisibility(id) {
    const input = document.getElementById(id);
    input.type = input.type === "password" ? "text" : "password";
}

// Alternar exibição das IAs
function toggleIAs() {
    const lista = document.getElementById("listaIAs");
    lista.style.display = lista.style.display === "none" ? "block" : "none";
}

// Simula o status da API
window.addEventListener("DOMContentLoaded", () => {
    const status = document.getElementById("apiStatus");
    status.textContent = "✅ Online com NovaDAX";
    status.style.color = "green";

    const log = document.getElementById("logOperacoes");
    const timestamp = new Date().toLocaleTimeString();
    log.innerHTML += `<p>[${timestamp}] Iniciado com sucesso. IAs em operação.</p>`;

    // Feedback ao salvar configurações
    const form = document.getElementById("configForm");
    form.addEventListener("submit", (e) => {
        e.preventDefault();
        const ts = new Date().toLocaleTimeString();
        log.innerHTML += `<p>[${ts}] Configurações salvas. Operação iniciada.</p>`;
        alert("✅ Configurações salvas com sucesso!");
    });
});
