from werkzeug.security import generate_password_hash, check_password_hash
from app.models.usuario import Usuario
from app.repository.usuario_repo import UsuarioRepo
from app import db
from datetime import datetime
from zoneinfo import ZoneInfo
from app.models.anonymization_log import AnonymizationLog


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
    def create_user(nome, email, senha, papel, especialidade=None, aceite_lgpd=False):
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
            especialidade=especialidade.strip() if especialidade else None,
            aceite_lgpd=bool(aceite_lgpd),
            aceite_lgpd_at=(datetime.now(ZoneInfo("America/Sao_Paulo")) if aceite_lgpd else None)
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
        # For LGPD: anonymize instead of deleting to preserve relations
        UsuarioService.anonimizar_usuario(user_id, anonimizado_por_id=user_id, motivo="Exclusão solicitada")

    @staticmethod
    def anonimizar_usuario(user_id, anonimizado_por_id=None, motivo="Solicitação"):
        user = UsuarioRepo.get_by_id(user_id)
        if not user:
            raise ValueError("Usuário não encontrado.")

        # remove personal data but keep relationships
        user.nome = "Usuário Anônimo"
        # If the DB requires email non-null, set a safe placeholder.
        try:
            nullable = Usuario.__table__.c.email.nullable
        except Exception:
            nullable = True
        if nullable:
            user.email = None
        else:
            user.email = f"deleted_{user.id}@anon.local"
        user.senha_hash = None
        user.especialidade = None
        user.aceite_lgpd = False
        user.aceite_lgpd_at = None
        user.anonimizado = True
        user.anonimizado_em = datetime.now(ZoneInfo("America/Sao_Paulo"))

        # create audit log
        try:
            log = AnonymizationLog(user_id=user.id, who_id=anonimizado_por_id, reason=motivo)
            db.session.add(log)
            db.session.commit()
        except Exception:
            db.session.rollback()
        return user
