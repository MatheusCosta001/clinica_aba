from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import pytz

db = SQLAlchemy()

# Função para retornar a hora de São Paulo
def agora_sp():
    return datetime.now(pytz.timezone("America/Sao_Paulo"))

class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(200), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)  # adm, coordenador, profissional
    criado_em = db.Column(db.DateTime, default=agora_sp)  # hora de SP

    evolucoes = db.relationship('Evolucao', backref='autor', lazy=True)

    def __repr__(self):
        return f"<Usuario {self.nome} ({self.tipo})>"

class Paciente(db.Model):
    __tablename__ = 'pacientes'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer)
    data_nascimento = db.Column(db.Date, nullable=False)
    diagnostico = db.Column(db.String(200))
    responsavel = db.Column(db.String(100))
    criado_em = db.Column(db.DateTime, default=agora_sp)  # hora de SP

    evolucoes = db.relationship('Evolucao', backref='paciente', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Paciente {self.nome}>"

class Evolucao(db.Model):
    __tablename__ = 'evolucoes'
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id', ondelete='CASCADE'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id', ondelete='CASCADE'), nullable=False)
    data_hora = db.Column(db.DateTime, default=agora_sp)  # hora de SP
    anotacao = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<Evolucao pac:{self.paciente_id} usr:{self.usuario_id} at {self.data_hora}>"
