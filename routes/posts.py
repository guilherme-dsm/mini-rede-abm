from flask import Blueprint, render_template, redirect, url_for, session

posts_bp = Blueprint("posts", __name__)

@posts_bp.route("/posts/mural")
def mural():
    if "morador_id" not in session:
        return redirect(url_for("auth.login"))
    return render_template("mural.html")