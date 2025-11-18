from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.services.evolucao_service import EvolucaoService
from app.services.paciente_service import PacienteService
from app.models.usuario import Usuario
from app.utils.auth_utils import login_required

evolucoes_bp = Blueprint("evolucoes", __name__, url_prefix="/evolucoes")



@evolucoes_bp.route("/")
@login_required
def index():
    """Lista os pacientes disponíveis para selecionar e ver as evoluções."""
    q = request.args.get('q', '').strip().lower()
    pacientes = PacienteService.listPacientes()
    if q:
        pacientes = [p for p in pacientes if q in (p.nome or '').lower() or q in (p.diagnostico or '').lower()]

    
    especialidades = [e[0] for e in Usuario.query.with_entities(Usuario.especialidade).filter(Usuario.especialidade != None).distinct().all()]

    return render_template("evolucoes/timeline.html", paciente=None, evolucoes=[], pacientes=pacientes, especialidades=especialidades, q=q)


@evolucoes_bp.route("/paciente/<int:paciente_id>")
@login_required
def timeline(paciente_id):
    paciente = PacienteService.getPaciente(paciente_id)
    if not paciente:
        flash("Paciente não encontrado.", "danger")
        return redirect(url_for("evolucoes.index"))

    especialidade_filter = request.args.get('especialidade_filter', '').strip()
    data_filter = request.args.get('data_filter', '')
    q = request.args.get('q', '').strip()

    evolucoes = EvolucaoService.listByPacienteWithFilters(paciente_id, especialidadeFilter=especialidade_filter, dateFilter=data_filter, q=q)

    
    especialidades = [e[0] for e in Usuario.query.with_entities(Usuario.especialidade).filter(Usuario.especialidade != None).distinct().all()]

    return render_template("evolucoes/timeline.html", paciente=paciente, evolucoes=evolucoes, pacientes=None, especialidades=especialidades, q=q)



@evolucoes_bp.route("/paciente/<int:paciente_id>/novo", methods=["GET", "POST"])
@login_required
def novo(paciente_id):
    paciente = PacienteService.get_paciente(paciente_id)
    if not paciente:
        flash("Paciente não encontrado.", "danger")
        return redirect(url_for("evolucoes.index"))

    if request.method == "POST":
        anotacao = request.form.get("anotacao")
        area = request.form.get("area")

        try:
            EvolucaoService.createEvolucao(paciente_id, session.get("user_id"), anotacao, area)
            flash("Evolução registrada com sucesso.", "success")
            return redirect(url_for("evolucoes.timeline", paciente_id=paciente_id))
        except Exception as e:
            flash(str(e), "danger")

    return render_template("evolucoes/novo.html", paciente=paciente)



@evolucoes_bp.route("/excluir/<int:evolucao_id>", methods=["POST"])
@login_required
def excluir_evolucao(evolucao_id):
    papel = session.get("papel")
    if papel not in ("adm", "coordenador"):
        flash("Acesso negado. Apenas ADM ou Coordenador podem excluir evoluções.", "danger")
        return redirect(url_for("evolucoes.index"))

    try:
        paciente_id = EvolucaoService.deleteEvolucao(evolucao_id, solicitadoPorId=session.get("user_id"))
        flash("Evolução excluída com sucesso.", "success")
        return redirect(url_for("evolucoes.timeline", paciente_id=paciente_id))
    except Exception as e:
        flash(str(e), "danger")
        return redirect(url_for("evolucoes.index"))
