from flask import Blueprint, request, jsonify
from models import db
from models.patient import Patient

patient_bp = Blueprint('patient', __name__)

@patient_bp.route("/patients", methods=["POST"])
def create_patient():
    data = request.get_json()
    patient = Patient(name=data['name'], age=data.get('age'), responsible=data.get('responsible'))
    db.session.add(patient)
    db.session.commit()
    return jsonify({"message": "Paciente criado!"})

@patient_bp.route("/patients", methods=["GET"])
def list_patients():
    patients = Patient.query.all()
    result = []
    for p in patients:
        result.append({"id": p.id, "name": p.name, "age": p.age, "responsible": p.responsible})
    return jsonify(result)
