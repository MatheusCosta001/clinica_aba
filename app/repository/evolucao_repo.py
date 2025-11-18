from app import db
from app.models.evolucao import Evolucao

class EvolucaoRepo:
    @staticmethod
    def listByPaciente(pacienteId):
        return Evolucao.query.filter_by(pacienteId=pacienteId).order_by(Evolucao.dataHora.desc()).all()

    @staticmethod
    def add(evolucao):
        db.session.add(evolucao)
        db.session.commit()
        return evolucao

    @staticmethod
    def getById(evolucao_id):
        if not evolucao_id:
            return None
        return db.session.get(Evolucao, evolucao_id)

    @staticmethod
    def delete(evolucao):
        db.session.delete(evolucao)
        db.session.commit()
        return True
