# TODO: rotas de autenticação (login, cadastro, logout)
from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from models.db import get_connection
import secrets
from datetime import datetime, timedelta
from email_utils import enviar_email_redefinicao
import psycopg2.errors

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]
        predio_id = request.form["predio_id"]
        apartamento = request.form["apartamento"]

        senha_hash = generate_password_hash(senha, method="pbkdf2:sha256")

        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO moradores (nome, email, senha_hash, predio_id, apartamento) VALUES (%s, %s, %s, %s, %s)",
                (nome, email, senha_hash, predio_id, apartamento)
            )
            conn.commit()
            conn.close()
            return redirect(url_for("auth.login"))
        except psycopg2.errors.UniqueViolation:
            conn.rollback()
            conn.close()

            conn2 = get_connection()
            cursor2 = conn2.cursor()
            cursor2.execute("SELECT id, nome, bloco FROM predios")
            predios = cursor2.fetchall()
            conn2.close()

            return render_template("cadastro.html", predios=predios, erro="Esse e-mail já está cadastrado")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, bloco FROM predios")
    predios = cursor.fetchall()
    conn.close()

    return render_template("cadastro.html", predios=predios)

@auth_bp.route("/login")
def login():
    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.pop("morador_id", None)
    return redirect(url_for("auth.login"))

@auth_bp.route("/esqueci-senha", methods=["GET", "POST"])
def esqueci_senha():
    if request.method == "POST":
        email = request.form["email"]

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM moradores WHERE email = %s", (email,))
        morador = cursor.fetchone()

        if morador:
            token = secrets.token_urlsafe(32)
            expira_em = datetime.now() + timedelta(minutes=30)

            cursor.execute(
                "INSERT INTO redefinicoes_senha (morador_id, token, expira_em) VALUES (%s, %s, %s)",
                (morador["id"], token, expira_em)
            )
            conn.commit()
            enviar_email_redefinicao(email, token)

        conn.close()
        return render_template("esqueci_senha.html", enviado=True)

    return render_template("esqueci_senha.html", enviado=False)


@auth_bp.route("/redefinir-senha/<token>", methods=["GET", "POST"])
def redefinir_senha(token):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM redefinicoes_senha WHERE token = %s", (token,))
    redefinicao = cursor.fetchone()

    if redefinicao is None or redefinicao["usado"] == 1:
        conn.close()
        return "Link inválido ou já utilizado", 400

    expira_em = redefinicao["expira_em"]
    if datetime.now() > expira_em:
        conn.close()
        return "Este link expirou. Solicite uma nova redefinição.", 400

    if request.method == "POST":
        nova_senha = request.form["senha"]
        senha_hash = generate_password_hash(nova_senha, method="pbkdf2:sha256")

        cursor.execute(
            "UPDATE moradores SET senha_hash = %s WHERE id = %s",
            (senha_hash, redefinicao["morador_id"])
        )
        cursor.execute(
            "UPDATE redefinicoes_senha SET usado = 1 WHERE id = %s",
            (redefinicao["id"],)
        )
        conn.commit()
        conn.close()
        return redirect(url_for("auth.login"))

    conn.close()
    return render_template("redefinir_senha.html", token=token)