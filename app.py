from flask import Flask, redirect, url_for, session
from routes.auth import auth_bp
from routes.posts import posts_bp
from routes.api import api_bp
from routes.perfil import perfil_bp
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")

app.register_blueprint(auth_bp)
app.register_blueprint(posts_bp)
app.register_blueprint(api_bp)
app.register_blueprint(perfil_bp)

@app.route("/")
def home():
    if session.get("morador_id"):
        return redirect(url_for("posts.mural"))
    return redirect(url_for("auth.login"))

if __name__ == "__main__":
    debug_mode = os.environ.get("FLASK_DEBUG", "False") == "True"
    app.run(debug=debug_mode, port=5001)