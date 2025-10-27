from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Evolucao, Paciente, db
from app.forms import EvolucaoForm

bp = Blueprint('evolucoes', __name__, url_prefix='/evolucoes')

@bp.route('/paciente/<int:paciente_id>')
@login_required
def timeline(paciente_id):
    paciente = Paciente.query.get_or_404(paciente_id)
    evolucoes = Evolucao.query.filter_by(paciente_id=paciente_id).order_by(Evolucao.data_hora.desc()).all()
    return render_template('evolucoes/timeline.html', paciente=paciente, evolucoes=evolucoes)

@bp.route('/paciente/<int:paciente_id>/nova', methods=['GET','POST'])
@login_required
def nova(paciente_id):
    paciente = Paciente.query.get_or_404(paciente_id)
    form = EvolucaoForm()
    if form.validate_on_submit():
        e = Evolucao(paciente_id=paciente.id, usuario_id=current_user.id, anotacao=form.anotacao.data)
        db.session.add(e)
        db.session.commit()
        flash('Evolução registrada', 'success')
        return redirect(url_for('evolucoes.timeline', paciente_id=paciente.id))
    return render_template('evolucoes/form.html', form=form, paciente=paciente)

@bp.route('/excluir/<int:id>', methods=['POST'])
@login_required
def excluir(id):
    e = Evolucao.query.get_or_404(id)
    if current_user.tipo not in ('adm','coordenador') and e.usuario_id != current_user.id:
        flash('Permissão negada', 'danger')
        return redirect(url_for('evolucoes.timeline', paciente_id=e.paciente_id))
    db.session.delete(e)
    db.session.commit()
    flash('Evolução excluída', 'success')
    return redirect(url_for('evolucoes.timeline', paciente_id=e.paciente_id))
