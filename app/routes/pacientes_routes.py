from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.services.paciente_service import PacienteService
from app.utils.auth_utils import login_required, role_required
from app import db
from app.models import Paciente, Evolucao

pacientes_bp = Blueprint("pacientes", __name__, url_prefix="/pacientes")


@pacientes_bp.route("/")
@login_required
def index():
    # filter: q (text search in nome, diagnostico, cidade, idade)
    q = request.args.get('q', '').strip()

    query = Paciente.query

    if q:
        like_q = f"%{q}%"
        try:
            # try numeric search for idade
            idade_search = int(q)
            query = query.filter((Paciente.nome.ilike(like_q)) | (Paciente.diagnostico.ilike(like_q)) | (Paciente.cidade.ilike(like_q)) | (Paciente.idade == idade_search))
        except ValueError:
            # not numeric, just text search
            query = query.filter((Paciente.nome.ilike(like_q)) | (Paciente.diagnostico.ilike(like_q)) | (Paciente.cidade.ilike(like_q)))

    pacientes = query.order_by(Paciente.nome).all()

    return render_template("pacientes/index.html", pacientes=pacientes, q=q)


@pacientes_bp.route("/excluidos")
@login_required
def excluidos():
    # apenas ADM pode acessar pacientes excluídos
    if session.get("papel") != "adm":
        flash("Permissão negada.", "danger")
        return redirect(url_for("pacientes.index"))
    pacientes = PacienteService.list_excluidos()
    return render_template("pacientes/excluidos.html", pacientes=pacientes)


@pacientes_bp.route("/excluidos/<int:paciente_id>")
@login_required
def detalhes_excluido(paciente_id):
    # apenas ADM pode acessar detalhes de pacientes excluídos
    if session.get("papel") != "adm":
        flash("Permissão negada.", "danger")
        return redirect(url_for("pacientes.index"))
    paciente = PacienteService.get_paciente(paciente_id)
    if not paciente or not paciente.anonimizado:
        flash("Paciente não encontrado ou não está anonimizado.", "danger")
        return redirect(url_for("pacientes.excluidos"))
    from app.services.evolucao_service import EvolucaoService
    evolucoes = EvolucaoService.list_by_paciente(paciente_id)
    return render_template("pacientes/detalhes_excluido.html", paciente=paciente, evolucoes=evolucoes)

@pacientes_bp.route("/novo", methods=["GET", "POST"])
@login_required
def novo():
    # apenas ADM e Coordenador podem cadastrar pacientes
    if session.get('papel') not in ('adm', 'coordenador'):
        flash('Permissão negada. Apenas ADM e Coordenador podem cadastrar pacientes.', 'danger')
        return redirect(url_for('pacientes.index'))
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
    # apenas ADM e Coordenador podem editar pacientes
    if session.get('papel') not in ('adm', 'coordenador'):
        flash('Permissão negada. Apenas ADM e Coordenador podem editar pacientes.', 'danger')
        return redirect(url_for('pacientes.index'))
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
