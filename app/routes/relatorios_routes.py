from flask import Blueprint, render_template, request, send_file, session, flash, redirect, url_for
from app.services.paciente_service import PacienteService
from app.services.evolucao_service import EvolucaoService
from app.utils.pdf_utils import gerar_relatorio_pdf
from io import BytesIO
from app.utils.auth_utils import login_required

relatorios_bp = Blueprint("relatorios", __name__, url_prefix="/relatorios")

@relatorios_bp.route("/<int:paciente_id>", methods=["GET", "POST"])
@login_required
def gerar(paciente_id):
    paciente = PacienteService.get_paciente(paciente_id)
    if not paciente:
        flash("Paciente não encontrado.", "danger")
        return redirect(url_for("pacientes.index"))
    if request.method == "POST":
        # recebe checkboxes com areas: ex: áreas selecionadas = ['psicologia','fonoaudiologia']
        areas = request.form.getlist("areas")
        todas = EvolucaoService.list_by_paciente(paciente_id)
        if areas:
            selecionadas = [e for e in todas if (e.area or "").lower() in [a.lower() for a in areas]]
        else:
            selecionadas = todas
        buffer = gerar_relatorio_pdf(paciente, selecionadas, session.get("user_nome", "Usuário"))
        return send_file(buffer, as_attachment=True, download_name=f"relatorio_{paciente.nome}.pdf", mimetype="application/pdf")
    # GET
    return render_template("relatorios/gerar.html", paciente=paciente)
