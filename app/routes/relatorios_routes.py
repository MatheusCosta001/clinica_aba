from flask import Blueprint, render_template, request, send_file, session, flash, redirect, url_for
from app.services.paciente_service import PacienteService
from app.services.evolucao_service import EvolucaoService
from app.utils.pdf_utils import gerar_relatorio_pdf
from io import BytesIO
from app.utils.auth_utils import login_required

relatorios_bp = Blueprint("relatorios", __name__, url_prefix="/relatorios")


# ✅ Quando o usuário clica em “Relatórios” no menu
@relatorios_bp.route("/", methods=["GET"])
@login_required
def index():
    """
    Mostra o template 'gerar.html' sem um paciente específico.
    Isso evita erro quando o usuário entra direto pela navbar.
    """
    return render_template("relatorios/gerar.html", paciente=None)


# ✅ Quando há paciente_id — gera o PDF
@relatorios_bp.route("/<int:paciente_id>", methods=["GET", "POST"])
@login_required
def gerar(paciente_id):
    paciente = PacienteService.get_paciente(paciente_id)
    if not paciente:
        flash("Paciente não encontrado.", "danger")
        return redirect(url_for("relatorios.index"))

    if request.method == "POST":
        areas = request.form.getlist("areas")
        todas = EvolucaoService.list_by_paciente(paciente_id)

        if areas:
            selecionadas = [e for e in todas if (e.area or "").lower() in [a.lower() for a in areas]]
        else:
            selecionadas = todas

        buffer = gerar_relatorio_pdf(
            paciente,
            selecionadas,
            session.get("user_nome", "Usuário")
        )

        return send_file(
            buffer,
            as_attachment=True,
            download_name=f"relatorio_{paciente.nome}.pdf",
            mimetype="application/pdf"
        )

    return render_template("relatorios/gerar.html", paciente=paciente)
