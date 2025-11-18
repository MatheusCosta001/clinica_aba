from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.services.paciente_service import PacienteService
from app.utils.auth_utils import login_required, role_required
from app import db
from app.models import Paciente, Evolucao

pacientes_bp = Blueprint("pacientes", __name__, url_prefix="/pacientes")


@pacientes_bp.route("/")
@login_required
def index():
    q = request.args.get('q', '').strip()
    pacientes = PacienteService.searchPacientes(q)
    return render_template("pacientes/index.html", pacientes=pacientes, q=q)


@pacientes_bp.route("/excluidos")
@login_required
def excluidos():
    
    if session.get("papel") != "adm":
        flash("Permissão negada.", "danger")
        return redirect(url_for("pacientes.index"))
    pacientes = PacienteService.listExcluidos()
    return render_template("pacientes/excluidos.html", pacientes=pacientes)

@pacientes_bp.route("/excluidos/<int:paciente_id>")
@login_required
def detalhes_excluido(paciente_id):
    
    if session.get("papel") != "adm":
        flash("Permissão negada.", "danger")
        return redirect(url_for("pacientes.index"))
    paciente = PacienteService.getPaciente(paciente_id)
    if not paciente or not paciente.anonimizado:
        flash("Paciente não encontrado ou não está anonimizado.", "danger")
        return redirect(url_for("pacientes.excluidos"))
    from app.services.evolucao_service import EvolucaoService
    evolucoes = EvolucaoService.listByPaciente(paciente_id)
    return render_template("pacientes/detalhes_excluido.html", paciente=paciente, evolucoes=evolucoes)

@pacientes_bp.route("/novo", methods=["GET", "POST"])
@login_required
def novo():
    
    if session.get('papel') not in ('adm', 'coordenador'):
        flash('Permissão negada. Apenas ADM e Coordenador podem cadastrar pacientes.', 'danger')
        return redirect(url_for('pacientes.index'))
    if request.method == "POST":
        data = {
            "nome": request.form.get("nome"),
            "dataNascimento": request.form.get("dataNascimento"),
            "diagnostico": request.form.get("diagnostico"),
            "responsavel": request.form.get("responsavel"),
            "cep": request.form.get("cep"),
            "rua": request.form.get("rua"),
            "bairro": request.form.get("bairro"),
            "cidade": request.form.get("cidade"),
            "uf": request.form.get("uf"),
        }
        try:
            PacienteService.createOrUpdate(data)
            flash("Paciente salvo.", "success")
            return redirect(url_for("pacientes.index"))
        except Exception as e:
            flash(str(e), "danger")
    return render_template("pacientes/novo.html")

@pacientes_bp.route("/<int:paciente_id>/editar", methods=["GET", "POST"])
@login_required
def editar(paciente_id):
    p = PacienteService.getPaciente(paciente_id)
    if not p:
        flash("Paciente não encontrado.", "danger")
        return redirect(url_for("pacientes.index"))
    
    if session.get('papel') not in ('adm', 'coordenador'):
        flash('Permissão negada. Apenas ADM e Coordenador podem editar pacientes.', 'danger')
        return redirect(url_for('pacientes.index'))
    if request.method == "POST":
        data = {
            "id": p.id,
            "nome": request.form.get("nome"),
            "dataNascimento": request.form.get("dataNascimento"),
            "diagnostico": request.form.get("diagnostico"),
            "responsavel": request.form.get("responsavel"),
            "cep": request.form.get("cep"),
            "rua": request.form.get("rua"),
            "bairro": request.form.get("bairro"),
            "cidade": request.form.get("cidade"),
            "uf": request.form.get("uf"),
        }
        try:
            PacienteService.createOrUpdate(data)
            flash("Paciente atualizado.", "success")
            return redirect(url_for("pacientes.index"))
        except Exception as e:
            flash(str(e), "danger")
    return render_template("pacientes/novo.html", paciente=p)

@pacientes_bp.route("/<int:paciente_id>/deletar", methods=["POST"])
@login_required
def deletar(paciente_id):
    
    if session.get("papel") not in ("adm", "coordenador"):
        flash("Permissão negada.", "danger")
        return redirect(url_for("pacientes.index"))
    try:
        PacienteService.deletePaciente(paciente_id)
        flash("Paciente removido.", "success")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for("pacientes.index"))
