from flask import Blueprint, render_template, request, send_file, session, flash, redirect, url_for
from app.services.paciente_service import PacienteService
from app.services.evolucao_service import EvolucaoService
from app.utils.pdf_utils import gerar_relatorio_pdf
from io import BytesIO
from app.utils.auth_utils import login_required
from app.models.relatorio import Relatorio
from app import db
from datetime import datetime
from zoneinfo import ZoneInfo

relatorios_bp = Blueprint("relatorios", __name__, url_prefix="/relatorios")

@relatorios_bp.route("/", methods=["GET"])
@login_required
def index():
    """
    Mostra o template 'gerar.html' sem um paciente específico.
    Isso evita erro quando o usuário entra direto pela navbar.
    """
    
    history = Relatorio.query.order_by(Relatorio.geradoEm.desc()).limit(50).all()
    return render_template("relatorios/gerar.html", paciente=None, history=history)

@relatorios_bp.route("/<int:paciente_id>", methods=["GET", "POST"])
@login_required
def gerar(paciente_id):
    paciente = PacienteService.getPaciente(paciente_id)
    if not paciente:
        flash("Paciente não encontrado.", "danger")
        return redirect(url_for("relatorios.index"))

    if request.method == "POST":
        areas = request.form.getlist("areas")
        data_inicio_str = request.form.get("dataInicio", "")
        data_fim_str = request.form.get("dataFim", "")
        comentarios = request.form.get("comentarios", "").strip()

        
        if not comentarios:
            comentarios = "Relatório gerado para visualização interna"

        todas = EvolucaoService.listByPaciente(paciente_id)

        
        if data_inicio_str or data_fim_str:
            from datetime import datetime
            try:
                data_inicio = datetime.strptime(data_inicio_str, "%Y-%m-%d").date() if data_inicio_str else None
                data_fim = datetime.strptime(data_fim_str, "%Y-%m-%d").date() if data_fim_str else None
                todas = [e for e in todas if (
                    (data_inicio is None or e.dataHora.date() >= data_inicio) and
                    (data_fim is None or e.dataHora.date() <= data_fim)
                )]
            except Exception:
                pass

        if areas:
            selecionadas = [e for e in todas if (e.area or "").lower() in [a.lower() for a in areas]]
        else:
            selecionadas = todas

        
        user_nome = session.get("user_nome", "Usuário")
        user_papel = session.get("papel", "")

        buffer = gerar_relatorio_pdf(
            paciente,
            selecionadas,
            user_nome,
            comentarios=comentarios,
            user_papel=user_papel,
            data_inicio=data_inicio_str,
            data_fim=data_fim_str
        )

        
        try:
            from datetime import datetime as dt
            data_inicio = dt.strptime(data_inicio_str, "%Y-%m-%d").date() if data_inicio_str else None
            data_fim = dt.strptime(data_fim_str, "%Y-%m-%d").date() if data_fim_str else None
            r = Relatorio(
                pacienteId=paciente.id,
                geradoPorId=session.get('user_id'),
                geradoEm=datetime.now(ZoneInfo('America/Sao_Paulo')),
                dataInicio=data_inicio,
                dataFim=data_fim,
                comentarios=comentarios
            )
            db.session.add(r)
            db.session.commit()
        except Exception:
            db.session.rollback()

        return send_file(
            buffer,
            as_attachment=True,
            download_name=f"relatorio_{paciente.nome}.pdf",
            mimetype="application/pdf"
        )

    return render_template("relatorios/gerar.html", paciente=paciente)
