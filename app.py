from flask import Flask, redirect, url_for, session
from routes.auth import auth_bp
from routes.posts import posts_bp
from routes.api import api_bp

app = Flask(__name__)
app.secret_key = "troque-essa-chave-depois"

app.register_blueprint(auth_bp)
app.register_blueprint(posts_bp)
app.register_blueprint(api_bp)

@app.route("/")
def home():
    if session.get("morador_id"):
        return redirect(url_for("posts.mural"))
    return redirect(url_for("auth.login"))

if __name__ == "__main__":
    app.run(debug=True, port=5001)
