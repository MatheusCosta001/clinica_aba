from app import db
from datetime import datetime
from zoneinfo import ZoneInfo


class Relatorio(db.Model):
    __tablename__ = 'relatorios'
    id = db.Column(db.Integer, primary_key=True)
    pacienteId = db.Column('pacienteId', db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    geradoPorId = db.Column('geradoPorId', db.Integer, db.ForeignKey('usuarios.id'), nullable=True)
    geradoEm = db.Column('geradoEm', db.DateTime, default=lambda: datetime.now(ZoneInfo('America/Sao_Paulo')), nullable=False)
    dataInicio = db.Column('dataInicio', db.Date, nullable=True)
    dataFim = db.Column('dataFim', db.Date, nullable=True)
    comentarios = db.Column(db.Text, nullable=True)

    paciente = db.relationship('Paciente')
    gerador = db.relationship('Usuario')

