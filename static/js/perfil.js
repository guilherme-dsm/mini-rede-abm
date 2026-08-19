function mostrarPreview(dataUrl) {
    const preview = document.getElementById("preview-foto");
    if (preview) {
        preview.src = dataUrl;
        return;
    }

    const novaImg = document.createElement("img");
    novaImg.id = "preview-foto";
    novaImg.className = "avatar-grande";
    novaImg.alt = "Foto de perfil";
    novaImg.src = dataUrl;
    avatarAntigo.replaceWith(novaImg);
}

function salvarPerfil(e) {
    e.preventDefault();

    const formData = new FormData();
    formData.append("nome", document.getElementById("input-nome").value);
    formData.append("email", document.getElementById("input-email").value);

    const arquivo = document.getElementById("input-foto").files[0];
    if (arquivo) {
        formData.append("foto", arquivo);
    }

    fetch("/api/perfil", {
        method: "PUT",
        body: formData
    })
        .then(resposta => resposta.json())
        .then(dados => {
            if (dados.erro) {
                mostrarToast(dados.erro, "erro");
                return;
            }
            mostrarToast(dados.mensagem, "sucesso");
        });
}

document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("form-perfil").addEventListener("submit", salvarPerfil);

    document.getElementById("input-foto").addEventListener("change", (e) => {
        const arquivo = e.target.files[0];
        if (!arquivo) return;

        const leitor = new FileReader();
        leitor.onload = (evento) => {
            mostrarPreview(evento.target.result);
        };
        leitor.readAsDataURL(arquivo);
    });
});