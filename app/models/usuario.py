from app import db
from datetime import datetime
from zoneinfo import ZoneInfo


class Usuario(db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=True)
    senha_hash = db.Column(db.String(200), nullable=True)
    papel = db.Column(db.String(50), nullable=False)
    especialidade = db.Column(db.String(100), nullable=True)
    aceite_lgpd = db.Column(db.Boolean, default=False, nullable=False)
    aceite_lgpd_at = db.Column(db.DateTime, nullable=True)
    anonimizado = db.Column(db.Boolean, default=False, nullable=False)
    anonimizado_em = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(ZoneInfo("America/Sao_Paulo")), nullable=False)

    evolucoes = db.relationship("Evolucao", back_populates="usuario", cascade="all, delete-orphan")
