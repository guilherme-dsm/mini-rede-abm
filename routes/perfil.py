from flask import Blueprint, render_template, redirect, url_for, session
from models.db import get_connection

perfil_bp = Blueprint("perfil", __name__)

@perfil_bp.route("/perfil")
def perfil():
    if "morador_id" not in session:
        return redirect(url_for("auth.login"))

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM moradores WHERE id = ?", (session["morador_id"],))
    morador = cursor.fetchone()
    conn.close()

    return render_template("perfil.html", morador=morador) 