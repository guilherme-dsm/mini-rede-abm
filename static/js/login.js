function fazerLogin(e) {
    e.preventDefault();

    const formData = new FormData();
    formData.append("email", document.getElementById("input-email-login").value);
    formData.append("senha", document.getElementById("input-senha-login").value);

    fetch("/api/login", {
        method: "POST",
        body: formData
    })
        .then(resposta => resposta.json())
        .then(dados => {
            if (dados.erro) {
                mostrarToast(dados.erro, "erro");
                return;
            }
            window.location.href = "/posts/mural";
        });
}

document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("form-login").addEventListener("submit", fazerLogin);
});