from app.services.evolucao_service import EvolucaoService
from app.services.paciente_service import PacienteService
from app.services.usuario_service import UsuarioService


def test_create_evolucao_and_list(app):
	with app.app_context():
		u = UsuarioService.createUser("Prof", "prof@example.com", "pw", "profissional", "Psico")
		p = PacienteService.createOrUpdate({"nome": "Paciente B"})
		e = EvolucaoService.createEvolucao(p.id, u.id, "Anotação teste", area="Área 1")
		assert e.id is not None
		items = EvolucaoService.listByPaciente(p.id)
		assert any(it.id == e.id for it in items)
