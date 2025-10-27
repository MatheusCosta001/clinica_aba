import os
import urllib.parse
from flask import Flask, redirect, url_for, Blueprint
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from .models import db, Usuario
from config import Config

# Inicializa extensões
login_manager = LoginManager()
bcrypt = Bcrypt()
migrate = Migrate()

def ensure_database(db_uri):
    """
    Tenta criar o banco se não existir.
    Funciona para URLs PostgreSQL do tipo postgresql://user:pass@host:port/dbname
    """
    try:
        import psycopg2
        parsed = urllib.parse.urlparse(db_uri)
        dbname = parsed.path.lstrip('/')
        user = parsed.username
        password = parsed.password
        host = parsed.hostname or 'localhost'
        port = parsed.port or 5432

        conn = psycopg2.connect(dbname='postgres', user=user, password=password, host=host, port=port)
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (dbname,))
        exists = cur.fetchone()
        if not exists:
            cur.execute(f'CREATE DATABASE "{dbname}"')
            print(f"✅ Banco criado: {dbname}")
        cur.close()
        conn.close()
    except Exception as e:
        print("⚠️ Não foi possível garantir criação automática do DB (verifique manualmente):", e)

def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config.from_object(Config)

    # Garante banco antes do SQLAlchemy inicializar
    db_uri = app.config.get('SQLALCHEMY_DATABASE_URI')
    if db_uri and db_uri.startswith('postgres'):
        ensure_database(db_uri)

    # Inicializa extensões
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)

    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    # Blueprints
    from app.routes import auth, pacientes, evolucoes, relatorios
    app.register_blueprint(auth.bp, url_prefix='/auth')
    app.register_blueprint(pacientes.bp, url_prefix='/pacientes')
    app.register_blueprint(evolucoes.bp, url_prefix='/evolucoes')
    app.register_blueprint(relatorios.bp, url_prefix='/relatorios')

    # Blueprint principal para rota "/"
    main_bp = Blueprint('main', __name__)

    @main_bp.route('/')
    def index():
        # Redireciona direto para a lista de pacientes
        return redirect(url_for('pacientes.listar'))

    app.register_blueprint(main_bp)

    # Cria tabelas e admin inicial
    with app.app_context():
        db.create_all()
        criar_admin_inicial()

    return app

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

def criar_admin_inicial():
    """Cria usuário admin padrão se não existir"""
    try:
        admin = Usuario.query.filter_by(email='admin@clinica.com').first()
        if not admin:
            from . import bcrypt
            senha_hash = bcrypt.generate_password_hash('admin123').decode('utf-8')
            novo = Usuario(nome='Administrador', email='admin@clinica.com', senha_hash=senha_hash, tipo='adm')
            db.session.add(novo)
            db.session.commit()
            print("✅ Usuário admin criado: admin@clinica.com / admin123")
    except Exception as e:
        print("⚠️ Erro ao criar admin inicial:", e)
