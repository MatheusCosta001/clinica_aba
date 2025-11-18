from app.services.paciente_service import PacienteService
from app.models.paciente import Paciente


def test_create_and_search_paciente(app):
	with app.app_context():
		data = {"nome": "Paciente A", "dataNascimento": "2010-01-01", "cidade": "CidadeX"}
		p = PacienteService.createOrUpdate(data)
		assert p.id is not None
		results = PacienteService.searchPacientes("Paciente")
		assert any(r.id == p.id for r in results)
