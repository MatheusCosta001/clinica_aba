from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.services.evolucao_service import EvolucaoService
from app.services.paciente_service import PacienteService
from app.utils.auth_utils import login_required

evolucoes_bp = Blueprint("evolucoes", __name__, url_prefix="/evolucoes")



@evolucoes_bp.route("/")
@login_required
def index():
    """Lista os pacientes disponíveis para selecionar e ver as evoluções."""
    pacientes = PacienteService.list_pacientes()
    return render_template("evolucoes/timeline.html", paciente=None, evolucoes=[], pacientes=pacientes)


@evolucoes_bp.route("/paciente/<int:paciente_id>")
@login_required
def timeline(paciente_id):
    paciente = PacienteService.get_paciente(paciente_id)
    if not paciente:
        flash("Paciente não encontrado.", "danger")
        return redirect(url_for("evolucoes.index"))

    evolucoes = EvolucaoService.list_by_paciente(paciente_id)
    return render_template("evolucoes/timeline.html", paciente=paciente, evolucoes=evolucoes, pacientes=None)



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
