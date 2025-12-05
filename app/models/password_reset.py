from app import db
from datetime import datetime
from zoneinfo import ZoneInfo

class PasswordResetToken(db.Model):
    __tablename__ = 'password_reset_tokens'
    id = db.Column(db.Integer, primary_key=True)
    usuarioId = db.Column('usuarioId', db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    token = db.Column(db.String(150), unique=True, nullable=False)
    expiracao = db.Column(db.DateTime, nullable=False)
    usado = db.Column(db.Boolean, default=False, nullable=False)
    criadoEm = db.Column('criadoEm', db.DateTime, default=lambda: datetime.now(ZoneInfo("America/Sao_Paulo")), nullable=False)

    usuario = db.relationship('Usuario', backref='reset_tokens')
