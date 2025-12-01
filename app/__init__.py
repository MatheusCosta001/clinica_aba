import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

db = SQLAlchemy()

def create_app():
    load_dotenv()

    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object("app.config.Config")

    db.init_app(app)

   
    from .routes.auth_routes import auth_bp
    from .routes.pacientes_routes import pacientes_bp
    from .routes.evolucoes_routes import evolucoes_bp
    from .routes.relatorios_routes import relatorios_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(pacientes_bp)
    app.register_blueprint(evolucoes_bp)
    app.register_blueprint(relatorios_bp)

    with app.app_context():
        
        db.create_all()
        
        from .models.usuario import Usuario
        from .services.usuario_service import UsuarioService

        if not Usuario.query.filter_by(email="admin@clinica.local").first():
            UsuarioService.createInitialAdmin()

    return app
