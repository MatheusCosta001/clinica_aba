from app.models.paciente import Paciente
from app.repository.paciente_repo import PacienteRepo
from datetime import datetime
from zoneinfo import ZoneInfo
from app import db

class PacienteService:
    @staticmethod
    def list_pacientes():
        return PacienteRepo.list_all()

    @staticmethod
    def list_excluidos():
        from app.models.paciente import Paciente as Pac
        return Pac.query.filter_by(anonimizado=True).order_by(Pac.nome).all()

    @staticmethod
    def get_paciente(paciente_id):
        return PacienteRepo.get_by_id(paciente_id)

    @staticmethod
    def create_or_update(data):
        
        if data.get("id"):
            p = PacienteRepo.get_by_id(data["id"])
            if not p:
                raise ValueError("Paciente não encontrado")
        else:
            p = Paciente()
        p.nome = data.get("nome")
       
        dn = data.get("data_nascimento")
        if dn:
            try:
                p.data_nascimento = datetime.strptime(dn, "%Y-%m-%d").date()
                
                hoje = datetime.today().date()
                p.idade = hoje.year - p.data_nascimento.year - ((hoje.month, hoje.day) < (p.data_nascimento.month, p.data_nascimento.day))
            except:
                p.data_nascimento = None
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
            db = __import__("app").app.db if False else None  
            from app import db as _db
            _db.session.commit()
        return p

    @staticmethod
    def delete_paciente(paciente_id):
        p = PacienteRepo.get_by_id(paciente_id)
        if not p:
            raise ValueError("Paciente não encontrado")
        
        p.nome = "Paciente Anônimo"
        p.data_nascimento = None
        p.idade = None
        p.diagnostico = None
        p.responsavel = None
        p.cep = None
        p.rua = None
        p.bairro = None
        p.cidade = None
        p.uf = None
        p.anonimizado = True
        p.anonimizado_em = datetime.now(ZoneInfo("America/Sao_Paulo"))
        db.session.commit()

    @staticmethod
    def anonimizar_paciente(paciente_id, motivo=None):
        p = PacienteRepo.get_by_id(paciente_id)
        if not p:
            raise ValueError("Paciente não encontrado")
        p.nome = "Paciente Anônimo"
        p.data_nascimento = None
        p.idade = None
        p.diagnostico = None
        p.responsavel = None
        p.cep = None
        p.rua = None
        p.bairro = None
        p.cidade = None
        p.uf = None
        p.anonimizado = True
        p.anonimizado_em = datetime.now(ZoneInfo("America/Sao_Paulo"))
        db.session.commit()
        return p
