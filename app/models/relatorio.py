from app import db
from datetime import datetime
from zoneinfo import ZoneInfo


class Relatorio(db.Model):
    __tablename__ = 'relatorios'
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    gerado_por_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)
    gerado_em = db.Column(db.DateTime, default=lambda: datetime.now(ZoneInfo('America/Sao_Paulo')), nullable=False)
    data_inicio = db.Column(db.Date, nullable=True)
    data_fim = db.Column(db.Date, nullable=True)
    comentarios = db.Column(db.Text, nullable=True)

    paciente = db.relationship('Paciente')
    gerador = db.relationship('Usuario')

