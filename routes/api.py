from flask import Blueprint, jsonify
from models.db import get_connection
from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from models.db import get_connection

api_bp = Blueprint("api", __name__, url_prefix="/api")

@api_bp.route("/posts")
def listar_posts():
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

    posts_json = [dict(post) for post in posts]
    return jsonify(posts_json)

@api_bp.route("/posts", methods=["POST"])
def criar_post():
    if "morador_id" not in session:
        return jsonify({"erro": "Não autenticado"}), 401

    dados = request.json
    categoria = dados.get("categoria")
    titulo = dados.get("titulo")
    conteudo = dados.get("conteudo")

    if not categoria or not titulo or not conteudo:
        return jsonify({"erro": "Campos obrigatórios faltando"}), 400

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO posts (autor_id, categoria, titulo, conteudo) VALUES (?, ?, ?, ?)",
        (session["morador_id"], categoria, titulo, conteudo)
    )
    conn.commit()
    novo_id = cursor.lastrowid
    conn.close()

    return jsonify({"id": novo_id, "mensagem": "Post criado"}), 201


@api_bp.route("/posts/<int:post_id>", methods=["PUT"])
def editar_post(post_id):
    if "morador_id" not in session:
        return jsonify({"erro": "Não autenticado"}), 401

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM posts WHERE id = ?", (post_id,))
    post = cursor.fetchone()

    if post is None:
        conn.close()
        return jsonify({"erro": "Post não encontrado"}), 404

    if post["autor_id"] != session["morador_id"]:
        conn.close()
        return jsonify({"erro": "Sem permissão"}), 403

    dados = request.json
    cursor.execute(
        "UPDATE posts SET categoria = ?, titulo = ?, conteudo = ? WHERE id = ?",
        (dados.get("categoria"), dados.get("titulo"), dados.get("conteudo"), post_id)
    )
    conn.commit()
    conn.close()

    return jsonify({"mensagem": "Post atualizado"})


@api_bp.route("/posts/<int:post_id>", methods=["DELETE"])
def deletar_post(post_id):
    if "morador_id" not in session:
        return jsonify({"erro": "Não autenticado"}), 401

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM posts WHERE id = ?", (post_id,))
    post = cursor.fetchone()

    if post is None:
        conn.close()
        return jsonify({"erro": "Post não encontrado"}), 404

    if post["autor_id"] != session["morador_id"]:
        conn.close()
        return jsonify({"erro": "Sem permissão"}), 403

    cursor.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    conn.commit()
    conn.close()

    return jsonify({"mensagem": "Post apagado"})