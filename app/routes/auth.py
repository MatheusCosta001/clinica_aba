from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models import Usuario, db
from app import bcrypt
from app.forms import LoginForm, RegisterForm
from flask import Blueprint, redirect, url_for

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    # Redireciona para a lista de pacientes ou dashboard
    return redirect(url_for('pacientes.listar'))

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Usuario.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.senha_hash, form.senha.data):
            login_user(user)
            return redirect(url_for('pacientes.listar'))
        flash('Credenciais inválidas', 'danger')
    return render_template('login.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@bp.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing = Usuario.query.filter_by(email=form.email.data).first()
        if existing:
            flash('E-mail já cadastrado', 'warning')
            return render_template('register.html', form=form)
        senha_hash = bcrypt.generate_password_hash(form.senha.data).decode('utf-8')
        usuario = Usuario(
            nome=form.nome.data,
            email=form.email.data,
            senha_hash=senha_hash,
            tipo=form.tipo.data
        )
        db.session.add(usuario)
        db.session.commit()
        flash('Usuário criado com sucesso', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)
