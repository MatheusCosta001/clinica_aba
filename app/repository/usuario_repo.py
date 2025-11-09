from app import db
from app.models.usuario import Usuario

class UsuarioRepo:
    @staticmethod
    def get_by_email(email):
        return Usuario.query.filter_by(email=email).first()

    @staticmethod
    def get_by_id(uid):
        return Usuario.query.get(uid)

    @staticmethod
    def add(usuario):
        db.session.add(usuario)
        db.session.commit()
