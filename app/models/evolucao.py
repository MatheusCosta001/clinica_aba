from app import db
from datetime import datetime
from zoneinfo import ZoneInfo


class Evolucao(db.Model):
    __tablename__ = "evolucoes"
    id = db.Column(db.Integer, primary_key=True)
    pacienteId = db.Column('pacienteId', db.Integer, db.ForeignKey("pacientes.id"), nullable=False)
    usuarioId = db.Column('usuarioId', db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    dataHora = db.Column('dataHora', db.DateTime, default=lambda: datetime.now(ZoneInfo("America/Sao_Paulo")))
    anotacao = db.Column(db.Text, nullable=False)
    area = db.Column(db.String(100), nullable=True)
    profissionalEspecialidade = db.Column('profissionalEspecialidade', db.String(100), nullable=True)

    paciente = db.relationship("Paciente", back_populates="evolucoes")
    usuario = db.relationship("Usuario", back_populates="evolucoes")
