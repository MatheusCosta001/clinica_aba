from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.services.usuario_service import UsuarioService
from app.models import Paciente, Evolucao, Usuario

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

        usuario = UsuarioService.authenticate(email, senha)
        if usuario:
            session["user_id"] = usuario.id
            session["user_nome"] = usuario.nome
            session["papel"] = usuario.papel

            flash(f"Bem-vindo(a), {usuario.nome}!", "success")
            return redirect(url_for("auth.dashboard"))
        else:
            flash("E-mail ou senha incorretos. Tente novamente.", "danger")

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Você saiu do sistema.", "info")
    return redirect(url_for("auth.login"))


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        senha = request.form.get("senha")
        papel = request.form.get("papel")
        especialidade = request.form.get("especialidade")

        try:
            UsuarioService.create_user(nome, email, senha, papel, especialidade)
            flash("Usuário criado com sucesso!", "success")
            return redirect(url_for("auth.login"))
        except Exception as e:
            flash(f"Erro ao criar usuário: {str(e)}", "danger")

    return render_template("register.html")


@auth_bp.route("/dashboard")
def dashboard():
    if not session.get("user_id"):
        flash("Você precisa estar logado para acessar o painel.", "warning")
        return redirect(url_for("auth.login"))

    total_pacientes = Paciente.query.count()
    total_evolucoes = Evolucao.query.count()
    total_usuarios = Usuario.query.count()

    return render_template(
        "dashboard.html",
        papel=session.get("papel"),
        user_nome=session.get("user_nome"),
        total_pacientes=total_pacientes,
        total_evolucoes=total_evolucoes,
        total_usuarios=total_usuarios,
    )


@auth_bp.route("/perfil", methods=["GET", "POST"])
def perfil():
    user_id = session.get("user_id")
    if not user_id:
        flash("Você precisa estar logado para acessar o perfil.", "warning")
        return redirect(url_for("auth.login"))

    user = UsuarioService.get_user_by_id(user_id)

    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]
        especialidade = request.form.get("especialidade")

        UsuarioService.update_user(user_id, nome, email, senha, especialidade)
        flash("Perfil atualizado com sucesso!", "success")
        return redirect(url_for("auth.perfil"))

    return render_template("perfil.html", user=user)


@auth_bp.route("/excluir_conta", methods=["POST"])
def excluir_conta():
    user_id = session.get("user_id")
    if not user_id:
        flash("Você precisa estar logado para excluir sua conta.", "warning")
        return redirect(url_for("auth.login"))

    UsuarioService.delete_user(user_id)
    session.clear()
    flash("Conta excluída com sucesso!", "success")
    return redirect(url_for("auth.login"))


