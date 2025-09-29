from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import db, bcrypt
from app.models import Usuario
from flask_login import login_user, logout_user, login_required, current_user

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("pacientes.listar"))
    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")
        user = Usuario.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.senha, senha):
            login_user(user)
            return redirect(url_for("pacientes.listar"))
        else:
            flash("Login ou senha incorretos", "danger")
    return render_template("login.html")

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        senha = request.form.get("senha")
        tipo = request.form.get("tipo")

        if Usuario.query.filter_by(email=email).first():
            flash("Email já cadastrado", "danger")
            return redirect(url_for("auth.register"))

        hashed = bcrypt.generate_password_hash(senha).decode("utf-8")
        user = Usuario(nome=nome, email=email, senha=hashed, tipo=tipo)
        db.session.add(user)
        db.session.commit()
        flash("Usuário cadastrado com sucesso!", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")
