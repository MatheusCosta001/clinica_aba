from app import db
from app.models.paciente import Paciente

class PacienteRepo:
    @staticmethod
    def listAll():
        return Paciente.query.order_by(Paciente.nome).all()

    @staticmethod
    def getById(pid):
        if not pid:
            return None
        return db.session.get(Paciente, pid)

    @staticmethod
    def add(paciente):
        db.session.add(paciente)
        db.session.commit()
        return paciente

    @staticmethod
    def delete(paciente):
        db.session.delete(paciente)
        db.session.commit()
