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
        if getattr(paciente, 'anonimizado', False):
            raise ValueError('Não é possível adicionar evoluções para pacientes inativos/anonimizados.')
        
        if usuario.papel == 'profissional':
            prof_espec = usuario.especialidade or ''
        elif usuario.papel == 'adm':
            prof_espec = 'ADM'
        elif usuario.papel == 'coordenador':
            prof_espec = 'Coordenador'
        else:
            prof_espec = usuario.especialidade or ''

        e = Evolucao(paciente_id=paciente_id, usuario_id=usuario_id, anotacao=anotacao, area=area, profissional_especialidade=prof_espec)
        EvolucaoRepo.add(e)
        return e    

    @staticmethod
    def delete_evolucao(evolucao_id, solicitado_por_id=None):
        e = EvolucaoRepo.get_by_id(evolucao_id)
        if not e:
            raise ValueError("Evolução não encontrada.")
        paciente_id = e.paciente_id
        EvolucaoRepo.delete(e)
        return paciente_id