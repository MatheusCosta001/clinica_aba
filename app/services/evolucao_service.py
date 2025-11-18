from app.models.evolucao import Evolucao
from app.repository.evolucao_repo import EvolucaoRepo
from app.repository.paciente_repo import PacienteRepo
from app.repository.usuario_repo import UsuarioRepo
from app import db

class EvolucaoService:
    @staticmethod
    def listByPaciente(pacienteId):
        return EvolucaoRepo.listByPaciente(pacienteId)

    @staticmethod
    def listByPacienteWithFilters(pacienteId, especialidadeFilter=None, dateFilter=None, q=None):
        """Retorna evoluções de um paciente aplicando filtros opcionais: especialidade, data e texto."""
        evolucoes = EvolucaoRepo.listByPaciente(pacienteId)

        if especialidadeFilter:
            ef = (especialidadeFilter or '').strip().lower()
            evolucoes = [e for e in evolucoes if ef in (e.profissionalEspecialidade or '').lower()]

        if dateFilter:
            from datetime import datetime
            try:
                target_date = datetime.strptime(dateFilter, '%Y-%m-%d').date()
                evolucoes = [e for e in evolucoes if e.dataHora.date() == target_date]
            except Exception:
                pass

        if q:
            qq = (q or '').strip().lower()
            evolucoes = [e for e in evolucoes if qq in (e.anotacao or '').lower() or qq in ((e.usuario.nome or '').lower())]

        return evolucoes

    @staticmethod
    def createEvolucao(pacienteId, usuarioId, anotacao, area=None):
        paciente = PacienteRepo.getById(pacienteId)
        usuario = UsuarioRepo.getById(usuarioId)
        if not paciente or not usuario:
            raise ValueError("Paciente ou usuário inválido")
        if getattr(paciente, 'anonimizado', False):
            raise ValueError('Não é possível adicionar evoluções para pacientes inativos/anonimizados.')
        

        role_map = {
            'adm': 'ADM',
            'coordenador': 'Coordenador',
            'profissional': usuario.especialidade or ''
        }
        prof_espec = role_map.get(usuario.papel, usuario.especialidade or '')

        e = Evolucao(pacienteId=pacienteId, usuarioId=usuarioId, anotacao=anotacao, area=area, profissionalEspecialidade=prof_espec)
        return EvolucaoRepo.add(e)

    @staticmethod
    def deleteEvolucao(evolucaoId, solicitadoPorId=None):
        e = EvolucaoRepo.getById(evolucaoId)
        if not e:
            raise ValueError("Evolução não encontrada.")
        pacienteId = e.pacienteId
        EvolucaoRepo.delete(e)
        return pacienteId