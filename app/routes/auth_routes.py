from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.services.usuario_service import UsuarioService

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/", methods=["GET"])
def home():
    if session.get("user_id"):
        return redirect(url_for("auth.dashboard"))
    return redirect(url_for("auth.login"))

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")
        user = UsuarioService.authenticate(email, senha)
        if user:
            session["user_id"] = user.id
            session["user_nome"] = user.nome
            session["papel"] = user.papel
            flash("Login feito com sucesso.", "success")
            return redirect(url_for("auth.dashboard"))
        flash("Credenciais inválidas.", "danger")
    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Deslogado.", "info")
    return redirect(url_for("auth.login"))

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    # permitimos apenas ADM ou coordenador criar usuarios pelo front? Para simplicidade permitimos qualquer user (ou admin via seed)
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        senha = request.form.get("senha")
        papel = request.form.get("papel")
        especialidade = request.form.get("especialidade")
        try:
            UsuarioService.create_user(nome, email, senha, papel, especialidade)
            flash("Usuário criado.", "success")
            return redirect(url_for("auth.login"))
        except Exception as e:
            flash(str(e), "danger")
    return render_template("register.html")

@auth_bp.route("/dashboard")
def dashboard():
    # dashboard simples por papel
    papel = session.get("papel")
    return render_template("dashboard.html", papel=papel, user_nome=session.get("user_nome"))
