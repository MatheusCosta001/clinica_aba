from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from config import Config

# --- Inicializa extensões GLOBALMENTE ---
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message_category = "info"

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # --- Inicializa extensões com a app ---
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # --- Importa blueprints ---
    from app.routes.auth import auth_bp
    from app.routes.pacientes import pacientes_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(pacientes_bp)

    # --- Cria tabelas e usuário admin automático ---
    with app.app_context():
        from app.models import Usuario

        db.create_all()

        # Cria admin se não existir
        admin = Usuario.query.filter_by(email="admin@clinica.com").first()
        if not admin:
            hashed = bcrypt.generate_password_hash("admin123").decode("utf-8")
            admin = Usuario(
                nome="Admin",
                email="admin@clinica.com",
                senha=hashed,
                tipo="ADM"
            )
            db.session.add(admin)
            db.session.commit()
            print("Usuário admin criado: admin@clinica.com / admin123")
        else:
            print("Usuário admin já existe.")

    return app
