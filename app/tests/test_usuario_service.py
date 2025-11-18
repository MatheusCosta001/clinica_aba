from app.services.usuario_service import UsuarioService
from app.models.usuario import Usuario
from app import db


def test_criar_usuario(app):
    with app.app_context():
        usuario = UsuarioService.createUser("João", "joao@example.com", "1234", "Psicólogo")
        assert usuario.id is not None
        assert usuario.nome == "João"


def test_buscar_usuario_por_email(app):
    with app.app_context():
        UsuarioService.createUser("Ana", "ana@example.com", "senha", "Coordenadora")
        usuario = Usuario.query.filter_by(email="ana@example.com").first()
        assert usuario is not None
        assert usuario.nome == "Ana"


def test_register_user_service_and_validation(app):
    with app.app_context():
        usuario = UsuarioService.registerUser("Test", "test@example.com", "pw", "pw", "profissional", None, True)
        assert usuario is not None
        assert usuario.email == "test@example.com"

        try:
            UsuarioService.registerUser("X", "x@example.com", "pw", "pw", "profissional", None, False)
            assert False, "Deveria ter lançado ValueError por LGPD"
        except ValueError:
            pass


def test_delete_account_with_password(app):
    with app.app_context():
        u = UsuarioService.createUser("Remover", "remover@example.com", "secret", "profissional")
        assert u is not None
        result = UsuarioService.deleteAccountWithPassword(u.id, "secret")
        assert result is True
        u_ref = db.session.get(Usuario, u.id)
        assert u_ref.anonimizado is True
