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
    pacientes = PacienteService.list_pacientes()
    if q:
        pacientes = [p for p in pacientes if q in (p.nome or '').lower() or q in (p.diagnostico or '').lower()]

    # gather existing especialidades from users to populate select in timeline view
    especialidades = [e[0] for e in Usuario.query.with_entities(Usuario.especialidade).filter(Usuario.especialidade != None).distinct().all()]

    return render_template("evolucoes/timeline.html", paciente=None, evolucoes=[], pacientes=pacientes, especialidades=especialidades, q=q)


@evolucoes_bp.route("/paciente/<int:paciente_id>")
@login_required
def timeline(paciente_id):
    paciente = PacienteService.get_paciente(paciente_id)
    if not paciente:
        flash("Paciente não encontrado.", "danger")
        return redirect(url_for("evolucoes.index"))

    evolucoes = EvolucaoService.list_by_paciente(paciente_id)

    # Apply filters if provided
    especialidade_filter = request.args.get('especialidade_filter', '').strip().lower()
    data_filter = request.args.get('data_filter', '')
    q = request.args.get('q', '').strip().lower()

    if especialidade_filter:
        evolucoes = [e for e in evolucoes if especialidade_filter in (e.profissional_especialidade or '').lower()]

    if data_filter:
        from datetime import datetime
        try:
            target_date = datetime.strptime(data_filter, '%Y-%m-%d').date()
            evolucoes = [e for e in evolucoes if e.data_hora.date() == target_date]
        except ValueError:
            pass

    if q:
        evolucoes = [e for e in evolucoes if q in (e.anotacao or '').lower() or q in ((e.usuario.nome or '').lower())]

    # provide list of specialties for the filter select
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
            EvolucaoService.create_evolucao(paciente_id, session.get("user_id"), anotacao, area)
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
        paciente_id = EvolucaoService.delete_evolucao(evolucao_id, solicitado_por_id=session.get("user_id"))
        flash("Evolução excluída com sucesso.", "success")
        return redirect(url_for("evolucoes.timeline", paciente_id=paciente_id))
    except Exception as e:
        flash(str(e), "danger")
        return redirect(url_for("evolucoes.index"))
