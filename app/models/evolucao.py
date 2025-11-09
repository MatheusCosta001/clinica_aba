from app import db
from datetime import datetime

class Evolucao(db.Model):
    __tablename__ = "evolucoes"
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey("pacientes.id"), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    data_hora = db.Column(db.DateTime, default=datetime.utcnow)
    anotacao = db.Column(db.Text, nullable=False)
    area = db.Column(db.String(100), nullable=True)  # ex: fonoaudiologia, psicologia

    paciente = db.relationship("Paciente", back_populates="evolucoes")
    usuario = db.relationship("Usuario", back_populates="evolucoes")
