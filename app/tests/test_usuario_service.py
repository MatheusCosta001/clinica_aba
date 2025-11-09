from app.services.usuario_service import UsuarioService
from app.models.usuario import Usuario
from app import db

def test_criar_usuario(app):
    with app.app_context():
        usuario = UsuarioService.create_user("João", "joao@example.com", "1234", "Psicólogo")
        assert usuario.id is not None
        assert usuario.nome == "João"

def test_buscar_usuario_por_email(app):
    with app.app_context():
        UsuarioService.create_user("Ana", "ana@example.com", "senha", "Coordenadora")
        usuario = Usuario.query.filter_by(email="ana@example.com").first()
        assert usuario is not None
        assert usuario.nome == "Ana"
