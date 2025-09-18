from . import db

class Patient(db.Model):
    __tablename__ = "patients"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    responsible = db.Column(db.String(100))

    def __repr__(self):
        return f"<Patient {self.name}>"
