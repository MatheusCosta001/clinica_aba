from flask import Blueprint, render_template, request, send_file
from flask_login import login_required
from app.models import Paciente, Evolucao
from app.utils import gerar_relatorio_pdf

bp = Blueprint('relatorios', __name__, url_prefix='/relatorios')

@bp.route('/<int:paciente_id>', methods=['GET','POST'])
@login_required
def gerar(paciente_id):
    paciente = Paciente.query.get_or_404(paciente_id)
    evolucoes = Evolucao.query.filter_by(paciente_id=paciente_id).order_by(Evolucao.data_hora.asc()).all()

    if request.method == 'POST':
        incluir = request.form.getlist('incluir')  # lista de especialidades/names
        if incluir:
            # filtra por autor.tipo ou por autor.nome — aqui simplificamos por nome/especialidade
            evolucoes = [e for e in evolucoes if (getattr(e.autor, 'tipo', None) in incluir) or (getattr(e.autor, 'nome', None) in incluir)]
        buffer = gerar_relatorio_pdf(paciente, evolucoes, gerador_nome='Sistema TCC')
        return send_file(buffer, mimetype='application/pdf', as_attachment=True, download_name=f'relatorio_{paciente.nome}.pdf')
    return render_template('relatorios/gerar.html', paciente=paciente)
