from app import db
from app.models.usuario import Usuario

class UsuarioRepo:
    @staticmethod
    def getByEmail(email):
        if not email:
            return None
        return Usuario.query.filter_by(email=email.strip().lower()).first()

    @staticmethod
    def getById(uid):
        if not uid:
            return None
        return db.session.get(Usuario, uid)

    @staticmethod
    def add(usuario):
        db.session.add(usuario)
        db.session.commit()
        return usuario
