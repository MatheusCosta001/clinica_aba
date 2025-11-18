from werkzeug.security import generate_password_hash, check_password_hash
from app.models.usuario import Usuario
from app.repository.usuario_repo import UsuarioRepo
from app import db
from datetime import datetime
from zoneinfo import ZoneInfo
from app.models.anonimizacao_log import AnonimizacaoLog


class UsuarioService:
    """Serviço responsável pelas regras de negócio relacionadas a usuários."""

    @staticmethod
    def createInitialAdmin():
        """Cria o usuário admin padrão caso ainda não exista."""
        admin_email = "admin@clinica.local"
        admin_existente = UsuarioRepo.getByEmail(admin_email)
        if not admin_existente:
            senhaHash = generate_password_hash("admin123")
            admin = Usuario(
                nome="Admin",
                email=admin_email.strip().lower(),
                senhaHash=senhaHash,
                papel="adm",
                especialidade=None
            )
            return UsuarioRepo.add(admin)
        return admin_existente

    @staticmethod
    def authenticate(email, senha):
        """
        Valida o login de um usuário com base no e-mail e senha.
        Retorna o usuário se for válido, senão None.
        """
        if not email or not senha:
            return None

        usuario = UsuarioRepo.getByEmail(email)
        if usuario and check_password_hash(usuario.senhaHash, senha):
            return usuario
        return None

    @staticmethod
    def createUser(nome, email, senha, papel, especialidade=None, aceiteLgpd=False):
        """
        Cria um novo usuário no sistema.
        - Verifica se o e-mail já existe.
        - Gera o hash da senha.
        - Retorna o usuário criado.
        """
        if not nome or not email or not senha or not papel:
            raise ValueError("Todos os campos obrigatórios devem ser preenchidos.")

        if UsuarioRepo.getByEmail(email):
            raise ValueError("E-mail já cadastrado.")

        senhaHash = generate_password_hash(senha)
        novo_usuario = Usuario(
            nome=nome.strip(),
            email=email.strip().lower(),
            senhaHash=senhaHash,
            papel=papel.strip(),
            especialidade=especialidade.strip() if especialidade else None,
            aceiteLgpd=bool(aceiteLgpd),
            aceiteLgpdEm=(datetime.now(ZoneInfo("America/Sao_Paulo")) if aceiteLgpd else None)
        )

        return UsuarioRepo.add(novo_usuario)

    @staticmethod
    def registerUser(nome, email, senha, confirmarSenha, papel, especialidade=None, aceiteLgpd=False):
        """Valida os dados de registro (senhas iguais, aceite LGPD) e cria o usuário."""
        if not confirmarSenha or confirmarSenha != senha:
            raise ValueError("As senhas não coincidem.")
        if not aceiteLgpd:
            raise ValueError("É necessário aceitar os termos e a política de privacidade.")
        return UsuarioService.createUser(nome, email, senha, papel, especialidade, aceiteLgpd=aceiteLgpd)

    @staticmethod
    def deleteAccountWithPassword(userId, senhaConfirm):
        """Autentica o usuário com a senha informada e anonimiza a conta se válida."""
        user = UsuarioRepo.getById(userId)
        if not user:
            raise ValueError("Usuário não encontrado.")

        authenticated = UsuarioService.authenticate(user.email, senhaConfirm)
        if not authenticated:
            raise ValueError("Senha incorreta.")
        UsuarioService.anonimizarUsuario(userId, anonimizado_por_id=userId, motivo="Auto-exclusão pelo usuário")
        return True

    @staticmethod
    def getById(userId):
        """Retorna um usuário pelo ID, ou None se não existir."""
        if not userId:
            return None
        return UsuarioRepo.getById(userId)

    @staticmethod
    def getUserById(userId):
        """Alias de getById, para compatibilidade com outros módulos."""
        return UsuarioService.getById(userId)

    @staticmethod
    def updateUser(userId, nome, email, senha=None, especialidade=None):
        """Atualiza as informações de um usuário existente."""
        usuario = UsuarioRepo.getById(userId)
        if not usuario:
            raise ValueError("Usuário não encontrado.")

        if nome:
            usuario.nome = nome.strip()
        if email:
            usuario.email = email.strip().lower()
        if senha:
            usuario.senhaHash = generate_password_hash(senha)
        if especialidade is not None:
            usuario.especialidade = especialidade.strip() if especialidade else None

        db.session.commit()
        return usuario

    @staticmethod
    def updateUserAdmin(userId, nome=None, email=None, papel=None, especialidade=None):
        """Atualiza um usuário com permissões de administrador (inclui mudança de papel)."""
        usuario = UsuarioRepo.getById(userId)
        if not usuario:
            raise ValueError("Usuário não encontrado.")
        if nome:
            usuario.nome = nome.strip()
        if email:
            usuario.email = email.strip().lower()
        if papel:
            usuario.papel = papel
        if especialidade is not None:
            usuario.especialidade = especialidade.strip() if especialidade else None
        db.session.commit()
        return usuario


    @staticmethod
    def deleteUser(userId):
        """Exclui um usuário existente."""
        user = UsuarioRepo.getById(userId)
        if not user:
            raise ValueError("Usuário não encontrado.")
        
        UsuarioService.anonimizarUsuario(userId, anonimizado_por_id=userId, motivo="Exclusão solicitada")
        return True

    @staticmethod
    def anonimizarUsuario(userId, anonimizado_por_id=None, motivo="Solicitação"):
        user = UsuarioRepo.getById(userId)
        if not user:
            raise ValueError("Usuário não encontrado.")

        
        user.nome = "Usuário Anônimo"
        
        try:
            nullable = Usuario.__table__.c.email.nullable
        except Exception:
            nullable = True
        if nullable:
            user.email = None
        else:
            user.email = f"deleted_{user.id}@anon.local"
        user.senhaHash = None
        user.especialidade = None
        user.aceiteLgpd = False
        user.aceiteLgpdEm = None
        user.anonimizado = True
        user.anonimizadoEm = datetime.now(ZoneInfo("America/Sao_Paulo"))

        

        try:
            log = AnonimizacaoLog(usuarioId=user.id, quemId=anonimizado_por_id, motivo=motivo)
            db.session.add(log)
            db.session.commit()
        except Exception:
            db.session.rollback()
        return user
