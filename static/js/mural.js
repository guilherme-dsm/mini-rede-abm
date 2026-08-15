const CORES_AVATAR = ["avatar-color-0", "avatar-color-1", "avatar-color-2", "avatar-color-3", "avatar-color-4"];
let postIdEmEdicao = null;

function apagarPost(postId) {
    if (!confirm("Tem certeza que deseja apagar este post?")) {
        return;
    }
    fetch(`/api/posts/${postId}`, { method: "DELETE" })
        .then(resposta => resposta.json())
        .then(dados => {
            if (dados.erro) {
                window.location.href = "/login";
                return;
            }
            carregarPosts();
        });
}

function editarPost(post) {
    postIdEmEdicao = post.id;
    document.getElementById("input-categoria").value = post.categoria;
    document.getElementById("input-titulo").value = post.titulo;
    document.getElementById("input-conteudo").value = post.conteudo;
    document.getElementById("btn-submit-post").textContent = "Salvar edição";

    const formContainer = document.getElementById("form-container");
    formContainer.style.display = "block";
    formContainer.scrollIntoView({ behavior: "smooth" });
}

function fecharFormulario() {
    document.getElementById("form-novo-post").reset();
    document.getElementById("form-container").style.display = "none";
    document.getElementById("btn-submit-post").textContent = "Publicar";
    postIdEmEdicao = null;
}

function criarElementoPost(post) {
    const card = document.createElement("article");
    card.className = "post-card";

    const header = document.createElement("div");
    header.className = "post-header";

    const avatar = document.createElement("div");
    avatar.className = "avatar " + CORES_AVATAR[post.autor_id % 5];
    avatar.textContent = post.autor_nome.charAt(0);

    const infoDiv = document.createElement("div");
    infoDiv.className = "post-author-info";

    const nomeStrong = document.createElement("strong");
    nomeStrong.textContent = post.autor_nome;

    const metaDiv = document.createElement("div");
    metaDiv.className = "post-meta";
    metaDiv.textContent = post.criado_em;

    infoDiv.appendChild(nomeStrong);
    infoDiv.appendChild(metaDiv);

    const badge = document.createElement("span");
    const categoriaClasse = post.categoria.toLowerCase().replace(/ /g, "-");
    badge.className = "badge badge-" + categoriaClasse;
    badge.textContent = post.categoria;

    header.appendChild(avatar);
    header.appendChild(infoDiv);
    header.appendChild(badge);

    const titulo = document.createElement("h3");
    titulo.className = "post-title";
    titulo.textContent = post.titulo;

    const conteudo = document.createElement("p");
    conteudo.className = "post-content";
    conteudo.textContent = post.conteudo;

    card.appendChild(header);
    card.appendChild(titulo);
    card.appendChild(conteudo);

    if (post.autor_id === MORADOR_ID_ATUAL) {
        const actions = document.createElement("div");
        actions.className = "post-actions";

        const botaoEditar = document.createElement("button");
        botaoEditar.className = "link-action";
        botaoEditar.textContent = "Editar";
        botaoEditar.addEventListener("click", () => editarPost(post));

        const botaoApagar = document.createElement("button");
        botaoApagar.className = "link-action link-danger";
        botaoApagar.textContent = "Apagar";
        botaoApagar.addEventListener("click", () => apagarPost(post.id));

        actions.appendChild(botaoEditar);
        actions.appendChild(botaoApagar);
        card.appendChild(actions);
    }

    return card;
}

function carregarPosts() {
    fetch("/api/posts")
        .then(resposta => resposta.json())
        .then(posts => {
            const container = document.getElementById("posts-container");
            container.innerHTML = "";

            if (posts.length === 0) {
                container.textContent = "Ainda não tem posts por aqui.";
                return;
            }

            posts.forEach(post => {
                const elemento = criarElementoPost(post);
                container.appendChild(elemento);
            });
        });
}

function salvarPost(e) {
    e.preventDefault();

    const categoria = document.getElementById("input-categoria").value;
    const titulo = document.getElementById("input-titulo").value;
    const conteudo = document.getElementById("input-conteudo").value;

    const url = postIdEmEdicao ? `/api/posts/${postIdEmEdicao}` : "/api/posts";
    const metodo = postIdEmEdicao ? "PUT" : "POST";

    fetch(url, {
        method: metodo,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ categoria, titulo, conteudo })
    })
        .then(resposta => resposta.json())
        .then(dados => {
            if (dados.erro) {
                window.location.href = "/login";
                return;
            }
            fecharFormulario();
            carregarPosts();
        });
}

function alternarFormulario(e) {
    const formContainer = document.getElementById("form-container");
    const estaAbrindo = formContainer.style.display === "none";

    if (estaAbrindo) {
        fecharFormulario();
        formContainer.style.display = "block";
    } else {
        formContainer.style.display = "none";
    }
}

document.addEventListener("DOMContentLoaded", () => {
    carregarPosts();
    document.getElementById("form-novo-post").addEventListener("submit", salvarPost);
    document.getElementById("btn-novo-post").addEventListener("click", alternarFormulario);
    setInterval(carregarPosts, 5000);
});

window.addEventListener("pageshow", (e) => {
    if (e.persisted) {
        location.reload();
    }
});