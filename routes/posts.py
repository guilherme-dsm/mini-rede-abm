from flask import Blueprint, render_template, request, redirect, url_for, session
from models.db import get_connection

posts_bp = Blueprint("posts", __name__)

CATEGORIAS = ["Aviso", "Compra e venda", "Evento", "Alerta"]

@posts_bp.route("/posts")
def feed():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT posts.*, moradores.nome AS autor_nome
        FROM posts
        JOIN moradores ON posts.autor_id = moradores.id
        ORDER BY posts.criado_em DESC
    """)
    posts = cursor.fetchall()
    conn.close()
    return render_template("feed.html", posts=posts)


@posts_bp.route("/posts/novo", methods=["GET", "POST"])
def novo_post():
    if "morador_id" not in session:
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        categoria = request.form["categoria"]
        titulo = request.form["titulo"]
        conteudo = request.form["conteudo"]

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO posts (autor_id, categoria, titulo, conteudo) VALUES (?, ?, ?, ?)",
            (session["morador_id"], categoria, titulo, conteudo)
        )
        conn.commit()
        conn.close()

        return redirect(url_for("posts.feed"))

    return render_template("post_form.html", categorias=CATEGORIAS, post=None)


@posts_bp.route("/posts/<int:post_id>/editar", methods=["GET", "POST"])
def editar_post(post_id):
    if "morador_id" not in session:
        return redirect(url_for("auth.login"))

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM posts WHERE id = ?", (post_id,))
    post = cursor.fetchone()

    if post is None:
        conn.close()
        return "Post não encontrado", 404

    if post["autor_id"] != session["morador_id"]:
        conn.close()
        return "Você não tem permissão para editar este post", 403

    if request.method == "POST":
        categoria = request.form["categoria"]
        titulo = request.form["titulo"]
        conteudo = request.form["conteudo"]

        cursor.execute(
            "UPDATE posts SET categoria = ?, titulo = ?, conteudo = ? WHERE id = ?",
            (categoria, titulo, conteudo, post_id)
        )
        conn.commit()
        conn.close()

        return redirect(url_for("posts.mural"))

    conn.close()
    return render_template("post_form.html", categorias=CATEGORIAS, post=post)


@posts_bp.route("/posts/<int:post_id>/deletar", methods=["POST"])
def deletar_post(post_id):
    if "morador_id" not in session:
        return redirect(url_for("auth.login"))

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM posts WHERE id = ?", (post_id,))
    post = cursor.fetchone()

    if post is None:
        conn.close()
        return "Post não encontrado", 404

    if post["autor_id"] != session["morador_id"]:
        conn.close()
        return "Você não tem permissão para apagar este post", 403

    cursor.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    conn.commit()
    conn.close()

    return redirect(url_for("posts.feed"))

@posts_bp.route("/posts/mural")
def mural():
    if "morador_id" not in session:
        return redirect(url_for("auth.login"))    
    return render_template("mural.html")