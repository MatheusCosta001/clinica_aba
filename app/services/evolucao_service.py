from app.models.evolucao import Evolucao
from app.repository.evolucao_repo import EvolucaoRepo
from app.repository.paciente_repo import PacienteRepo
from app.repository.usuario_repo import UsuarioRepo
from app import db

class EvolucaoService:
    @staticmethod
    def list_by_paciente(paciente_id):
        return EvolucaoRepo.list_by_paciente(paciente_id)

    @staticmethod
    def create_evolucao(paciente_id, usuario_id, anotacao, area=None):
        paciente = PacienteRepo.get_by_id(paciente_id)
        usuario = UsuarioRepo.get_by_id(usuario_id)
        if not paciente or not usuario:
            raise ValueError("Paciente ou usuário inválido")
        e = Evolucao(paciente_id=paciente_id, usuario_id=usuario_id, anotacao=anotacao, area=area)
        EvolucaoRepo.add(e)
        return e    