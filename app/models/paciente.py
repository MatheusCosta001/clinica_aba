from app import db
from datetime import date, datetime
from zoneinfo import ZoneInfo


class Paciente(db.Model):
    __tablename__ = "pacientes"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    dataNascimento = db.Column('dataNascimento', db.Date, nullable=True)
    idade = db.Column(db.Integer, nullable=True)
    diagnostico = db.Column(db.String(300), nullable=True)
    responsavel = db.Column(db.String(200), nullable=True)
    cep = db.Column(db.String(10), nullable=True)
    rua = db.Column(db.String(200), nullable=True)
    bairro = db.Column(db.String(150), nullable=True)
    cidade = db.Column(db.String(150), nullable=True)
    uf = db.Column(db.String(2), nullable=True)
    anonimizado = db.Column(db.Boolean, default=False, nullable=False)
    anonimizadoEm = db.Column('anonimizadoEm', db.DateTime, nullable=True)

    evolucoes = db.relationship("Evolucao", back_populates="paciente", cascade="all, delete-orphan")
