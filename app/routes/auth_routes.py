from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.services.usuario_service import UsuarioService
from app.models import Paciente, Evolucao, Usuario
from app import db
from datetime import datetime

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
        confirmar = request.form.get("confirmar_senha")
        papel = request.form.get("papel")
        especialidade = request.form.get("especialidade")
        aceite_lgpd = True if request.form.get("aceite_lgpd") == "on" else False

        
        if not confirmar or confirmar != senha:
            flash("As senhas não coincidem.", "danger")
            return render_template("register.html")
        if not aceite_lgpd:
            flash("É necessário aceitar os termos e a política de privacidade.", "warning")
            return render_template("register.html")

        try:
            UsuarioService.create_user(nome, email, senha, papel, especialidade, aceite_lgpd=aceite_lgpd)
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
        nome = request.form.get("nome")
        email = request.form.get("email")
        senha = request.form.get("senha")
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
    senha_confirm = request.form.get("senha_confirmacao")
    if not senha_confirm:
        flash("É necessário informar a senha para confirmar a exclusão.", "warning")
        return redirect(url_for("auth.perfil"))

    user = UsuarioService.authenticate(UsuarioService.get_user_by_id(user_id).email, senha_confirm)
    if not user:
        flash("Senha incorreta.", "danger")
        return redirect(url_for("auth.perfil"))

    UsuarioService.anonimizar_usuario(user_id, anonimizado_por_id=user_id, motivo="Auto-exclusão pelo usuário")
    session.clear()
    flash("Conta anonimizada com sucesso.", "success")
    return redirect(url_for("auth.login"))


@auth_bp.route("/admin/anonimizar_usuario/<int:target_user_id>", methods=["POST"])
def admin_anonimizar_usuario(target_user_id):
   
    if session.get("papel") != "adm":
        flash("Acesso negado. Apenas administradores podem anonimizar usuários.", "danger")
        return redirect(url_for("auth.dashboard"))

    admin_id = session.get("user_id")
    try:
        UsuarioService.anonimizar_usuario(target_user_id, anonimizado_por_id=admin_id, motivo="Anonimização por ADM")
        flash("Usuário anonimizado com sucesso.", "success")
    except Exception as e:
        flash(f"Falha ao anonimizar usuário: {str(e)}", "danger")

    return redirect(url_for("auth.dashboard"))


@auth_bp.route('/admin/usuarios')
def admin_list_usuarios():
    
    if session.get('papel') != 'adm':
        flash('Acesso negado. Apenas administradores podem acessar esta página.', 'danger')
        return redirect(url_for('auth.dashboard'))

    q = request.args.get('q', '').strip().lower()
    papel_filter = request.args.get('papel_filter', '').strip().lower()
    especialidade_filter = request.args.get('especialidade_filter', '').strip()
    date_filter = request.args.get('date_filter', '').strip()

    query = Usuario.query
    if q:
        query = query.filter((Usuario.nome.ilike(f"%{q}%")) | (Usuario.email.ilike(f"%{q}%")))
    if papel_filter:
        query = query.filter(Usuario.papel == papel_filter)
    if especialidade_filter:
        query = query.filter(Usuario.especialidade == especialidade_filter)
    if date_filter:
        try:
            d = datetime.strptime(date_filter, '%Y-%m-%d')
            query = query.filter(db.func.date(Usuario.created_at) == d.date())
        except Exception:
            pass

    usuarios = query.order_by(Usuario.id.asc()).all()

    
    especialidades = [e[0] for e in Usuario.query.with_entities(Usuario.especialidade).filter(Usuario.especialidade != None).distinct().all()]

    return render_template('admin/usuarios.html', usuarios=usuarios, especialidades=especialidades, q=q, papel_filter=papel_filter, especialidade_filter=especialidade_filter, date_filter=date_filter)


@auth_bp.route('/admin/usuarios/<int:uid>')
def admin_view_usuario(uid):
    if session.get('papel') != 'adm':
        flash('Acesso negado.', 'danger')
        return redirect(url_for('auth.dashboard'))
    u = Usuario.query.get(uid)
    if not u:
        flash('Usuário não encontrado.', 'danger')
        return redirect(url_for('auth.admin_list_usuarios'))
    evolucoes = Evolucao.query.filter_by(usuario_id=u.id).order_by(Evolucao.data_hora.desc()).all()
    return render_template('admin/usuario_detalhes.html', usuario=u, evolucoes=evolucoes)


@auth_bp.route('/admin/usuarios/<int:uid>/editar', methods=['GET', 'POST'])
def admin_edit_usuario(uid):
    if session.get('papel') != 'adm':
        flash('Acesso negado.', 'danger')
        return redirect(url_for('auth.dashboard'))
    u = Usuario.query.get(uid)
    if not u:
        flash('Usuário não encontrado.', 'danger')
        return redirect(url_for('auth.admin_list_usuarios'))
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        papel = request.form.get('papel')
        especialidade = request.form.get('especialidade')
        try:
            UsuarioService.update_user(u.id, nome, email, None, especialidade)
            
            u.papel = papel or u.papel
            u.especialidade = especialidade or u.especialidade
            from app import db
            db.session.commit()
            flash('Usuário atualizado.', 'success')
            return redirect(url_for('auth.admin_list_usuarios'))
        except Exception as e:
            flash(str(e), 'danger')
    return render_template('admin/usuario_editar.html', usuario=u)

@auth_bp.route("/lgpd")
def lgpd():
    return render_template("lgpd.html")



