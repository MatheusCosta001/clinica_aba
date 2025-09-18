from . import db
from datetime import datetime

class Evolution(db.Model):
    __tablename__ = "evolutions"
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    professional = db.Column(db.String(100))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    patient = db.relationship("Patient", backref=db.backref("evolutions", lazy=True))

    def __repr__(self):
        return f"<Evolution {self.id} Patient {self.patient_id}>"
