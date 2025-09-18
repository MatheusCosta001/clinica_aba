from flask import Blueprint, request, jsonify
from models import db
from models.evolution import Evolution
from models.patient import Patient

evolution_bp = Blueprint('evolution', __name__)

@evolution_bp.route("/evolutions", methods=["POST"])
def create_evolution():
    data = request.get_json()
    evolution = Evolution(
        patient_id=data['patient_id'],
        professional=data['professional'],
        notes=data['notes']
    )
    db.session.add(evolution)
    db.session.commit()
    return jsonify({"message": "Evolução registrada!"})

@evolution_bp.route("/evolutions/<int:patient_id>", methods=["GET"])
def get_evolutions(patient_id):
    evolutions = Evolution.query.filter_by(patient_id=patient_id).all()
    result = []
    for e in evolutions:
        result.append({
            "id": e.id,
            "professional": e.professional,
            "notes": e.notes,
            "created_at": e.created_at
        })
    return jsonify(result)
