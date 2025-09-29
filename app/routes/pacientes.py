from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app import db
from app.models import Paciente

pacientes_bp = Blueprint("pacientes", __name__, url_prefix="/pacientes")

@pacientes_bp.route("/")
@login_required
def listar():
    pacientes = Paciente.query.all()
    return render_template("pacientes/listar.html", pacientes=pacientes)

@pacientes_bp.route("/novo", methods=["GET", "POST"])
@login_required
def novo():
    if request.method == "POST":
        nome = request.form.get("nome")
        idade = request.form.get("idade")
        data_nascimento = request.form.get("data_nascimento")
        diagnostico = request.form.get("diagnostico")
        responsavel = request.form.get("responsavel")

        paciente = Paciente(
            nome=nome,
            idade=int(idade),
            data_nascimento=data_nascimento,
            diagnostico=diagnostico,
            responsavel=responsavel
        )
        db.session.add(paciente)
        db.session.commit()
        flash("Paciente cadastrado com sucesso!", "success")
        return redirect(url_for("pacientes.listar"))

    return render_template("pacientes/form.html")
