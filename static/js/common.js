function mostrarToast(mensagem, tipo = "sucesso") {
    const toast = document.getElementById("toast");
    toast.textContent = mensagem;
    toast.className = "toast toast-" + tipo + " toast-visivel";

    setTimeout(() => {
        toast.className = "toast toast-" + tipo;
    }, 3000);
}

document.addEventListener("DOMContentLoaded", () => {
    const btnNovoPost = document.getElementById("btn-novo-post");
    if (btnNovoPost) {
        btnNovoPost.addEventListener("click", () => {
            if (typeof alternarFormulario === "function") { //essa condicao avalia se existe a funcao alternarFormulario e como ela só existe no mural nao irá abir o formulario caso nao esteja no feed
                alternarFormulario();
            } else {
                window.location.href = "/posts/mural?novo=1"; //comando para navegar para outra URL, nesse caso para o feed
            }
        });
    }
});