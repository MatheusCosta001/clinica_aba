from app import db
from app.models.evolucao import Evolucao

class EvolucaoRepo:
    @staticmethod
    def list_by_paciente(paciente_id):
        return Evolucao.query.filter_by(paciente_id=paciente_id).order_by(Evolucao.data_hora.desc()).all()

    @staticmethod
    def add(evolucao):
        db.session.add(evolucao)
        db.session.commit()
