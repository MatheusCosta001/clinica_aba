from app import db
from datetime import datetime
from zoneinfo import ZoneInfo


class AnonymizationLog(db.Model):
    __tablename__ = 'anonymizations'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    who_id = db.Column(db.Integer, nullable=True)
    reason = db.Column(db.String(300), nullable=True)
    when = db.Column(db.DateTime, default=lambda: datetime.now(ZoneInfo('America/Sao_Paulo')))
