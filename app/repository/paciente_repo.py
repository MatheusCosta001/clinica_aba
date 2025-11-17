from app import db
from app.models.paciente import Paciente

class PacienteRepo:
    @staticmethod
    def list_all():
        return Paciente.query.order_by(Paciente.nome).all()

    @staticmethod
    def get_by_id(pid):
        return Paciente.query.get(pid)

    @staticmethod
    def add(paciente):
        db.session.add(paciente)
        db.session.commit()

    @staticmethod
    def delete(paciente):
        db.session.delete(paciente)
        db.session.commit()
