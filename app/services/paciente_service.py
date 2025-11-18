from app.models.paciente import Paciente
from app.repository.paciente_repo import PacienteRepo
from datetime import datetime
from zoneinfo import ZoneInfo
from app import db


class PacienteService:
    """Regras de negócio relacionadas a pacientes.

    Mantemos métodos curtos e com responsabilidade única. Funções públicas
    expõem operações claras (listar, buscar, salvar, deletar/anonimizar).
    """

    @staticmethod
    def listPacientes():
        return PacienteRepo.listAll()

    @staticmethod
    def listExcluidos():
        return Paciente.query.filter_by(anonimizado=True).order_by(Paciente.nome).all()

    @staticmethod
    def getPaciente(pacienteId):
        if not pacienteId:
            return None
        return PacienteRepo.getById(pacienteId)

    @staticmethod
    def searchPacientes(queryText):
        """Busca pacientes por nome, diagnóstico, cidade ou idade (quando for número)."""
        q = (queryText or '').strip()
        query = Paciente.query
        if not q:
            return query.order_by(Paciente.nome).all()
        like_q = f"%{q}%"
        try:
            idadeSearch = int(q)
            query = query.filter((Paciente.nome.ilike(like_q)) | (Paciente.diagnostico.ilike(like_q)) | (Paciente.cidade.ilike(like_q)) | (Paciente.idade == idadeSearch))
        except ValueError:
            query = query.filter((Paciente.nome.ilike(like_q)) | (Paciente.diagnostico.ilike(like_q)) | (Paciente.cidade.ilike(like_q)))
        return query.order_by(Paciente.nome).all()

    @staticmethod
    def createOrUpdate(data):
        """Cria ou atualiza um paciente. Validações básicas e commits centralizados."""
        if not data or not data.get('nome'):
            raise ValueError('O nome do paciente é obrigatório.')

        if data.get("id"):
            p = PacienteRepo.getById(data["id"])
            if not p:
                raise ValueError("Paciente não encontrado")
        else:
            p = Paciente()

        p.nome = data.get("nome").strip()

        dn = data.get("dataNascimento")
        if dn:
            try:
                p.dataNascimento = datetime.strptime(dn, "%Y-%m-%d").date()
                hoje = datetime.today().date()
                p.idade = hoje.year - p.dataNascimento.year - ((hoje.month, hoje.day) < (p.dataNascimento.month, p.dataNascimento.day))
            except Exception:
                p.dataNascimento = None
                p.idade = None
        else:
            p.dataNascimento = None
            p.idade = None

        p.diagnostico = data.get("diagnostico")
        p.responsavel = data.get("responsavel")
        p.cep = data.get("cep")
        p.rua = data.get("rua")
        p.bairro = data.get("bairro")
        p.cidade = data.get("cidade")
        p.uf = data.get("uf")

        if not data.get("id"):
            PacienteRepo.add(p)
        else:
            db.session.commit()
        return p

    @staticmethod
    def _anonymize_entity(paciente, motivo=None):
        """Anonymiza os dados do paciente em memória e persiste a alteração."""
        paciente.nome = "Paciente Anônimo"
        paciente.dataNascimento = None
        paciente.idade = None
        paciente.diagnostico = None
        paciente.responsavel = None
        paciente.cep = None
        paciente.rua = None
        paciente.bairro = None
        paciente.cidade = None
        paciente.uf = None
        paciente.anonimizado = True
        paciente.anonimizadoEm = datetime.now(ZoneInfo("America/Sao_Paulo"))
        db.session.commit()
        return paciente

    @staticmethod
    def deletePaciente(pacienteId):
        p = PacienteRepo.getById(pacienteId)
        if not p:
            raise ValueError("Paciente não encontrado")
        return PacienteService._anonymize_entity(p, motivo="Remoção")

    @staticmethod
    def anonimizarPaciente(pacienteId, motivo=None):
        p = PacienteRepo.getById(pacienteId)
        if not p:
            raise ValueError("Paciente não encontrado")
        return PacienteService._anonymize_entity(p, motivo=motivo)
