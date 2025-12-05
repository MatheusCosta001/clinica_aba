from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.services.usuario_service import UsuarioService
from app.utils.email_utils import send_email
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
        aceiteLgpd = True if request.form.get("aceiteLgpd") == "on" else False

        try:
            UsuarioService.registerUser(nome, email, senha, confirmar, papel, especialidade, aceiteLgpd=aceiteLgpd)
            flash("Usuário criado com sucesso!", "success")
            return redirect(url_for("auth.login"))
        except Exception as e:
            flash(str(e), "danger")

    return render_template("register.html")


@auth_bp.route('/esqueci_senha', methods=['POST'])
def esqueci_senha():
    email = request.form.get('email')
    try:
        token = UsuarioService.iniciar_recuperacao_senha(email)
        link = f"{request.url_root.rstrip('/')}/resetar_senha/{token}"
        assunto = 'Recuperação de senha - Clínica ABA'
        texto = f'Para redefinir sua senha, acesse: {link}'
        html = f'<p>Para redefinir sua senha, clique no link abaixo:</p><p><a href="{link}">{link}</a></p>'
        try:
            send_email(email, assunto, html, texto)
            flash('Enviamos um link de recuperação para o e-mail informado.', 'info')
        except Exception as e:
            print('Falha ao enviar e-mail via SMTP:', str(e))
            print(f'Link de recuperação (fallback) para {email}: {link}')
            flash('Não foi possível enviar o e-mail. O link de recuperação foi exibido no console do servidor para testes.', 'warning')
    except Exception as e:
        flash(str(e), 'danger')
    return redirect(url_for('auth.login'))


@auth_bp.route('/resetar_senha/<token>', methods=['GET', 'POST'])
def resetar_senha(token):
    if request.method == 'POST':
        nova = request.form.get('nova_senha')
        confirmar = request.form.get('confirmar_nova_senha')
        if not nova or not confirmar or nova != confirmar:
            flash('Senhas não coincidem.', 'danger')
            return redirect(request.url)
        try:
            UsuarioService.resetar_senha(token, nova)
            flash('Senha alterada com sucesso. Faça login com a nova senha.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            flash(str(e), 'danger')
            return redirect(request.url)
    return render_template('resetar_senha.html', token=token)


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


@auth_bp.route("/perfil", methods=["GET"])
def perfil():
    user_id = session.get("user_id")
    if not user_id:
        flash("Você precisa estar logado para acessar o perfil.", "warning")
        return redirect(url_for("auth.login"))

    user = UsuarioService.getUserById(user_id)
    if not user:
        session.clear()
        flash("Usuário não encontrado. Faça login novamente.", "warning")
        return redirect(url_for("auth.login"))
    return render_template("perfil.html", user=user)


@auth_bp.route('/perfil/alterar_senha', methods=['POST'])
def alterar_senha():
    user_id = session.get('user_id')
    if not user_id:
        flash('Você precisa estar logado.', 'warning')
        return redirect(url_for('auth.login'))
    senha_atual = request.form.get('senha_atual')
    nova = request.form.get('nova_senha')
    confirmar = request.form.get('confirmar_nova_senha')
    if not senha_atual or not nova or not confirmar or nova != confirmar:
        flash('Dados inválidos ou senhas não coincidem.', 'danger')
        return redirect(url_for('auth.perfil'))
    try:
        UsuarioService.alterar_senha(user_id, senha_atual, nova)
        flash('Senha alterada com sucesso.', 'success')
    except Exception as e:
        flash(str(e), 'danger')
    return redirect(url_for('auth.perfil'))


@auth_bp.route('/perfil/alterar_email', methods=['POST'])
def alterar_email():
    user_id = session.get('user_id')
    if not user_id:
        flash('Você precisa estar logado.', 'warning')
        return redirect(url_for('auth.login'))
    senha = request.form.get('senha_confirmacao')
    novo_email = request.form.get('novo_email')
    if not senha or not novo_email:
        flash('Dados inválidos.', 'danger')
        return redirect(url_for('auth.perfil'))
    try:
        UsuarioService.alterar_email(user_id, senha, novo_email)
        flash('E-mail alterado com sucesso.', 'success')
    except Exception as e:
        flash(str(e), 'danger')
    return redirect(url_for('auth.perfil'))


@auth_bp.route("/excluir_conta", methods=["POST"])
def excluir_conta():
    user_id = session.get("user_id")
    if not user_id:
        flash("Você precisa estar logado para excluir sua conta.", "warning")
        return redirect(url_for("auth.login"))
    senha_confirm = request.form.get("senha_confirmacao")
    senha_confirm_repeat = request.form.get("senha_confirmacao_repeat")
    try:
        if not senha_confirm or not senha_confirm_repeat:
            raise ValueError("É necessário informar e confirmar a senha para confirmar a exclusão.")
        if senha_confirm != senha_confirm_repeat:
            raise ValueError("As senhas informadas não coincidem.")
        UsuarioService.deleteAccountWithPassword(user_id, senha_confirm)
        session.clear()
        flash("Conta anonimizada com sucesso.", "success")
        return redirect(url_for("auth.login"))
    except Exception as e:
        flash(str(e), "danger")
        return redirect(url_for("auth.perfil"))


@auth_bp.route("/admin/anonimizar_usuario/<int:target_user_id>", methods=["POST"])
def admin_anonimizar_usuario(target_user_id):
   
    if session.get("papel") != "adm":
        flash("Acesso negado. Apenas administradores podem anonimizar usuários.", "danger")
        return redirect(url_for("auth.dashboard"))

    admin_id = session.get("user_id")
    try:
        UsuarioService.anonimizarUsuario(target_user_id, anonimizado_por_id=admin_id, motivo="Anonimização por ADM")
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
            query = query.filter(db.func.date(Usuario.criadoEm) == d.date())
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
    u = db.session.get(Usuario, uid)
    if not u:
        flash('Usuário não encontrado.', 'danger')
        return redirect(url_for('auth.admin_list_usuarios'))
    evolucoes = Evolucao.query.filter_by(usuarioId=u.id).order_by(Evolucao.dataHora.desc()).all()
    return render_template('admin/usuario_detalhes.html', usuario=u, evolucoes=evolucoes)


@auth_bp.route('/admin/usuarios/<int:uid>/editar', methods=['GET', 'POST'])
def admin_edit_usuario(uid):
    if session.get('papel') != 'adm':
        flash('Acesso negado.', 'danger')
        return redirect(url_for('auth.dashboard'))
    u = db.session.get(Usuario, uid)
    if not u:
        flash('Usuário não encontrado.', 'danger')
        return redirect(url_for('auth.admin_list_usuarios'))
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        papel = request.form.get('papel')
        especialidade = request.form.get('especialidade')
        try:
            UsuarioService.updateUserAdmin(u.id, nome=nome, email=email, papel=papel, especialidade=especialidade)
            flash('Usuário atualizado.', 'success')
            return redirect(url_for('auth.admin_list_usuarios'))
        except Exception as e:
            flash(str(e), 'danger')
    return render_template('admin/usuario_editar.html', usuario=u)

@auth_bp.route("/lgpd")
def lgpd():
    return render_template("lgpd.html")



