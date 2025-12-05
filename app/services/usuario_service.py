from werkzeug.security import generate_password_hash, check_password_hash
from app.models.usuario import Usuario
from app.models.password_reset import PasswordResetToken
from app.repository.usuario_repo import UsuarioRepo
from app import db
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from app.models.anonimizacao_log import AnonimizacaoLog
import re
import uuid


class UsuarioService:

    @staticmethod
    def createInitialAdmin():
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
        if not email or not senha:
            return None

        usuario = UsuarioRepo.getByEmail(email)
        if usuario and check_password_hash(usuario.senhaHash, senha):
            return usuario
        return None

    @staticmethod
    def _normalize_name(nome: str) -> str:
        if not nome:
            return nome
        parts = [p.strip() for p in nome.split() if p.strip()]
        lower_words = {"da", "de", "do", "dos", "das", "e"}
        normalized = []
        for i, p in enumerate(parts):
            low = p.lower()
            if i != 0 and low in lower_words:
                normalized.append(low)
            else:
                normalized.append(low.capitalize())
        return " ".join(normalized)

    @staticmethod
    def _validate_password(senha: str):
        if not senha or len(senha) < 6:
            raise ValueError("A senha deve ter no mínimo 6 caracteres e conter ao menos 1 caractere especial.")
        if not re.search(r"[^A-Za-z0-9]", senha):
            raise ValueError("A senha deve ter no mínimo 6 caracteres e conter ao menos 1 caractere especial.")

    @staticmethod
    def createUser(nome, email, senha, papel, especialidade=None, aceiteLgpd=False):
        if not nome or not email or not senha or not papel:
            raise ValueError("Todos os campos obrigatórios devem ser preenchidos.")

        if UsuarioRepo.getByEmail(email):
            raise ValueError("E-mail já cadastrado.")

        UsuarioService._validate_password(senha)

        senhaHash = generate_password_hash(senha)
        nome_norm = UsuarioService._normalize_name(nome)
        if papel and papel.strip().lower() == 'adm':
            raise ValueError('Não é permitido criar usuário com papel de administrador via cadastro público.')

        novo_usuario = Usuario(
            nome=nome_norm,
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
        if not confirmarSenha or confirmarSenha != senha:
            raise ValueError("As senhas não coincidem.")
        if not aceiteLgpd:
            raise ValueError("É necessário aceitar os termos e a política de privacidade.")
        return UsuarioService.createUser(nome, email, senha, papel, especialidade, aceiteLgpd=aceiteLgpd)

    @staticmethod
    def deleteAccountWithPassword(userId, senhaConfirm):
        user = UsuarioRepo.getById(userId)
        if not user:
            raise ValueError("Usuário não encontrado.")

        authenticated = UsuarioService.authenticate(user.email, senhaConfirm)
        if not authenticated:
            raise ValueError("Senha incorreta.")
        UsuarioService.anonimizarUsuario(userId, anonimizado_por_id=userId, motivo="Auto-exclusão pelo usuário")
        return True

    @staticmethod
    def iniciar_recuperacao_senha(email: str):
        if not email:
            raise ValueError('E-mail inválido')
        user = UsuarioRepo.getByEmail(email)
        if not user:
            raise ValueError('E-mail não cadastrado')
        token = str(uuid.uuid4())
        expires = datetime.now(ZoneInfo("America/Sao_Paulo")) + timedelta(hours=2)
        pr = PasswordResetToken(usuarioId=user.id, token=token, expiracao=expires)
        db.session.add(pr)
        db.session.commit()
        return token

    @staticmethod
    def resetar_senha(token: str, nova_senha: str):
        if not token or not nova_senha:
            raise ValueError('Token ou senha inválidos')
        pr = db.session.query(PasswordResetToken).filter_by(token=token).first()
        if not pr:
            raise ValueError('Token inválido ou expirado')
        if pr.usado:
            raise ValueError('Token já utilizado')
        agora = datetime.now(ZoneInfo("America/Sao_Paulo"))
        expiracao = pr.expiracao
        if expiracao.tzinfo is None:
            expiracao = expiracao.replace(tzinfo=ZoneInfo("America/Sao_Paulo"))
        if expiracao < agora:
            raise ValueError('Token expirado')
        UsuarioService._validate_password(nova_senha)
        user = UsuarioRepo.getById(pr.usuarioId)
        if not user:
            raise ValueError('Usuário não encontrado')
        user.senhaHash = generate_password_hash(nova_senha)
        pr.usado = True
        db.session.commit()
        return True

    @staticmethod
    def alterar_senha(usuarioId: int, senha_atual: str, nova_senha: str):
        user = UsuarioRepo.getById(usuarioId)
        if not user:
            raise ValueError('Usuário não encontrado')
        if not check_password_hash(user.senhaHash or '', senha_atual):
            raise ValueError('Senha atual incorreta')
        UsuarioService._validate_password(nova_senha)
        user.senhaHash = generate_password_hash(nova_senha)
        db.session.commit()
        return True

    @staticmethod
    def alterar_email(usuarioId: int, senha_confirmacao: str, novo_email: str):
        user = UsuarioRepo.getById(usuarioId)
        if not user:
            raise ValueError('Usuário não encontrado')
        if not check_password_hash(user.senhaHash or '', senha_confirmacao):
            raise ValueError('Senha incorreta')
        if UsuarioRepo.getByEmail(novo_email):
            raise ValueError('E-mail já cadastrado')
        user.email = novo_email.strip().lower()
        db.session.commit()
        return True

    @staticmethod
    def getById(userId):
        if not userId:
            return None
        return UsuarioRepo.getById(userId)

    @staticmethod
    def getUserById(userId):
        return UsuarioService.getById(userId)

    @staticmethod
    def updateUser(userId, nome, email, senha=None, especialidade=None):
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
