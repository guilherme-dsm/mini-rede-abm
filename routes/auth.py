# TODO: rotas de autenticação (login, cadastro, logout)
from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from models.db import get_connection

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
        cursor.execute(
            "INSERT INTO moradores (nome, email, senha_hash, predio_id, apartamento) VALUES (?, ?, ?, ?, ?)",(nome, email, senha_hash, predio_id, apartamento)
        )
        conn.commit()
        conn.close()    

        return redirect(url_for("auth.login"))
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, bloco FROM predios")
    predios = cursor.fetchall()
    conn.close()

    return render_template("cadastro.html", predios=predios)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM moradores WHERE email = ?", (email,))
        morador = cursor.fetchone()
        conn.close()

        if morador and check_password_hash(morador["senha_hash"], senha):
            session["morador_id"] = morador["id"]
            return redirect(url_for("posts.mural"))
        
        return "Email ou senha incorretos", 401
    
    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.pop("morador_id", None)
    return redirect(url_for("auth.login"))