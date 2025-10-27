from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Paciente, db
from app.forms import PacienteForm

bp = Blueprint('pacientes', __name__, url_prefix='/pacientes')

@bp.route('/')
@login_required
def listar():
    pacientes = Paciente.query.order_by(Paciente.nome.asc()).all()
    return render_template('pacientes/listar.html', pacientes=pacientes)

@bp.route('/novo', methods=['GET','POST'])
@login_required
def novo():
    form = PacienteForm()
    if form.validate_on_submit():
        p = Paciente(
            nome=form.nome.data,
            data_nascimento=form.data_nascimento.data,
            idade=form.idade.data,
            diagnostico=form.diagnostico.data,
            responsavel=form.responsavel.data
        )
        db.session.add(p)
        db.session.commit()
        flash('Paciente criado', 'success')
        return redirect(url_for('pacientes.listar'))
    return render_template('pacientes/form.html', form=form, paciente=None)

@bp.route('/editar/<int:id>', methods=['GET','POST'])
@login_required
def editar(id):
    p = Paciente.query.get_or_404(id)
    form = PacienteForm(obj=p)
    if form.validate_on_submit():
        form.populate_obj(p)
        db.session.commit()
        flash('Paciente atualizado', 'success')
        return redirect(url_for('pacientes.listar'))
    return render_template('pacientes/form.html', form=form, paciente=p)

@bp.route('/excluir/<int:id>', methods=['POST'])
@login_required
def excluir(id):
    p = Paciente.query.get_or_404(id)
    # apenas adm/coordenador podem excluir pacientes
    if current_user.tipo not in ('adm','coordenador'):
        flash('Permissão negada', 'danger')
        return redirect(url_for('pacientes.listar'))
    db.session.delete(p)
    db.session.commit()
    flash('Paciente excluído', 'success')
    return redirect(url_for('pacientes.listar'))
