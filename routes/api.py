from flask import Blueprint, jsonify
from models.db import get_connection
from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from models.db import get_connection
import os
from werkzeug.utils import secure_filename
import sqlite3

api_bp = Blueprint("api", __name__, url_prefix="/api")

@api_bp.route("/posts")
def listar_posts():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT posts.*, moradores.nome AS autor_nome, moradores.foto_perfil AS autor_foto
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

@api_bp.route("/perfil", methods=["PUT"])
def atualizar_perfil():
    if "morador_id" not in session:
        return jsonify({"erro": "Não autenticado"}), 401

    nome = request.form.get("nome")
    email = request.form.get("email")

    conn = get_connection()
    cursor = conn.cursor()

    foto = request.files.get("foto")
    if foto and foto.filename:
        extensoes_permitidas = {"png", "jpg", "jpeg", "gif", "webp"}
        extensao = foto.filename.rsplit(".", 1)[-1].lower() if "." in foto.filename else "" #pega o formato do arquivo#

        if extensao not in extensoes_permitidas:
            conn.close()
            return jsonify({"erro": "Formato de imagem não permitido"}), 400 

        nome_arquivo = secure_filename(f"morador_{session['morador_id']}.{extensao}") #limpa texto removendo caractere perigoso ou invalido e garante que cada morador tenha sua foto com arquivo nomeado com seu respectivo id, evitando sobrescrever arquivo
        pasta_upload = os.path.join("static", "uploads", "perfil") #cria todas as pastas do caminho especificado para uploads das fotos dos usuarios
        os.makedirs(pasta_upload, exist_ok=True)
        foto.save(os.path.join(pasta_upload, nome_arquivo))

        caminho_relativo = f"uploads/perfil/{nome_arquivo}" #como na url_for por padrao ja entrará em static, salvamos dessa outra forma no bdd, pois se nao ficaria duplicado e quebraria
        cursor.execute("UPDATE moradores SET foto_perfil = ? WHERE id = ?", (caminho_relativo, session["morador_id"]))

    try:
        cursor.execute("UPDATE moradores SET nome = ?, email = ? WHERE id = ?", (nome, email, session["morador_id"]))
        conn.commit()
    except sqlite3.IntegrityError: #unique no bdd
        conn.close()
        return jsonify({"erro": "Esse e-mail já está em uso"}), 400

    conn.close()
    return jsonify({"mensagem": "Perfil atualizado com sucesso"})