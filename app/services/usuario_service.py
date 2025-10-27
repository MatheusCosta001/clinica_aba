from werkzeug.security import generate_password_hash, check_password_hash
from app.models.usuario import Usuario
from app.repository.usuario_repo import UsuarioRepo
from app import db

class UsuarioService:
    @staticmethod
    def create_initial_admin():
        # cria admin padrão se não existir
        if not UsuarioRepo.get_by_email("admin@clinica.local"):
            senha_hash = generate_password_hash("admin123")
            admin = Usuario(nome="Admin", email="admin@clinica.local", senha_hash=senha_hash, papel="adm", especialidade=None)
            db.session.add(admin)
            db.session.commit()
            return admin
        return None

    @staticmethod
    def authenticate(email, senha):
        u = UsuarioRepo.get_by_email(email)
        if u and check_password_hash(u.senha_hash, senha):
            return u
        return None

    @staticmethod
    def create_user(nome, email, senha, papel, especialidade=None):
        if UsuarioRepo.get_by_email(email):
            raise ValueError("Email já cadastrado")
        senha_hash = generate_password_hash(senha)
        user = Usuario(nome=nome, email=email, senha_hash=senha_hash, papel=papel, especialidade=especialidade)
        UsuarioRepo.add(user)
        return user
