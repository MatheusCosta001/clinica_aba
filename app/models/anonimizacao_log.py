from app import db
from datetime import datetime
from zoneinfo import ZoneInfo


class AnonimizacaoLog(db.Model):
    __tablename__ = 'anonimizacao'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, nullable=False)
    quem_id = db.Column(db.Integer, nullable=True)
    motivo = db.Column(db.String(300), nullable=True)
    quando = db.Column(db.DateTime, default=lambda: datetime.now(ZoneInfo('America/Sao_Paulo')))
