from werkzeug.security import generate_password_hash, check_password_hash
from app.models.usuario import Usuario
from app.repository.usuario_repo import UsuarioRepo
from app import db


class UsuarioService:
    """Serviço responsável pelas regras de negócio relacionadas a usuários."""

    @staticmethod
    def create_initial_admin():
        """Cria o usuário admin padrão caso ainda não exista."""
        admin_email = "admin@clinica.local"
        admin_existente = UsuarioRepo.get_by_email(admin_email)

        if not admin_existente:
            senha_hash = generate_password_hash("admin123")
            admin = Usuario(
                nome="Admin",
                email=admin_email,
                senha_hash=senha_hash,
                papel="adm",
                especialidade=None
            )
            db.session.add(admin)
            db.session.commit()
            return admin
        return None

    @staticmethod
    def authenticate(email, senha):
        """
        Valida o login de um usuário com base no e-mail e senha.
        Retorna o usuário se for válido, senão None.
        """
        if not email or not senha:
            return None

        usuario = UsuarioRepo.get_by_email(email)
        if usuario and check_password_hash(usuario.senha_hash, senha):
            return usuario
        return None

    @staticmethod
    def create_user(nome, email, senha, papel, especialidade=None):
        """
        Cria um novo usuário no sistema.
        - Verifica se o e-mail já existe.
        - Gera o hash da senha.
        - Retorna o usuário criado.
        """
        if not nome or not email or not senha or not papel:
            raise ValueError("Todos os campos obrigatórios devem ser preenchidos.")

        if UsuarioRepo.get_by_email(email):
            raise ValueError("E-mail já cadastrado.")

        senha_hash = generate_password_hash(senha)
        novo_usuario = Usuario(
            nome=nome.strip(),
            email=email.strip().lower(),
            senha_hash=senha_hash,
            papel=papel.strip(),
            especialidade=especialidade.strip() if especialidade else None
        )

        UsuarioRepo.add(novo_usuario)
        return novo_usuario

    @staticmethod
    def get_by_id(user_id):
        """Retorna um usuário pelo ID, ou None se não existir."""
        if not user_id:
            return None
        return UsuarioRepo.get_by_id(user_id)

    @staticmethod
    def get_user_by_id(user_id):
        """Alias de get_by_id, para compatibilidade com outros módulos."""
        return UsuarioService.get_by_id(user_id)

    @staticmethod
    def update_user(user_id, nome, email, senha=None, especialidade=None):
        """Atualiza as informações de um usuário existente."""
        usuario = UsuarioRepo.get_by_id(user_id)
        if not usuario:
            raise ValueError("Usuário não encontrado.")

        if nome:
            usuario.nome = nome.strip()
        if email:
            usuario.email = email.strip().lower()
        if senha:
            usuario.senha_hash = generate_password_hash(senha)
        if especialidade is not None:
            usuario.especialidade = especialidade.strip() if especialidade else None

        db.session.commit()
        return usuario


    @staticmethod
    def delete_user(user_id):
        """Exclui um usuário existente."""
        user = UsuarioRepo.get_by_id(user_id)
        if not user:
            raise ValueError("Usuário não encontrado.")

        db.session.delete(user)
        db.session.commit()
