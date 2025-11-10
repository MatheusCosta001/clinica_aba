from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.services.paciente_service import PacienteService
from app.utils.auth_utils import login_required, role_required

pacientes_bp = Blueprint("pacientes", __name__, url_prefix="/pacientes")

@pacientes_bp.route("/")
@login_required
def index():
    pacientes = PacienteService.list_pacientes()
    return render_template("pacientes/index.html", pacientes=pacientes)

@pacientes_bp.route("/novo", methods=["GET", "POST"])
@login_required
def novo():
    if request.method == "POST":
        data = {
            "nome": request.form.get("nome"),
            "data_nascimento": request.form.get("data_nascimento"),
            "diagnostico": request.form.get("diagnostico"),
            "responsavel": request.form.get("responsavel"),
            "cep": request.form.get("cep"),
            "rua": request.form.get("rua"),
            "bairro": request.form.get("bairro"),
            "cidade": request.form.get("cidade"),
            "uf": request.form.get("uf"),
        }
        try:
            PacienteService.create_or_update(data)
            flash("Paciente salvo.", "success")
            return redirect(url_for("pacientes.index"))
        except Exception as e:
            flash(str(e), "danger")
    return render_template("pacientes/novo.html")

@pacientes_bp.route("/<int:paciente_id>/editar", methods=["GET", "POST"])
@login_required
def editar(paciente_id):
    p = PacienteService.get_paciente(paciente_id)
    if not p:
        flash("Paciente não encontrado.", "danger")
        return redirect(url_for("pacientes.index"))
    if request.method == "POST":
        data = {
            "id": p.id,
            "nome": request.form.get("nome"),
            "data_nascimento": request.form.get("data_nascimento"),
            "diagnostico": request.form.get("diagnostico"),
            "responsavel": request.form.get("responsavel"),
            "cep": request.form.get("cep"),
            "rua": request.form.get("rua"),
            "bairro": request.form.get("bairro"),
            "cidade": request.form.get("cidade"),
            "uf": request.form.get("uf"),
        }
        try:
            PacienteService.create_or_update(data)
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
        PacienteService.delete_paciente(paciente_id)
        flash("Paciente removido.", "success")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for("pacientes.index"))
