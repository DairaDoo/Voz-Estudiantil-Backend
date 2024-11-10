import datetime
from app.utils.db import db

class Professors_Questions(db.Model):
    __tablename__ = 'Professors_Questions'
    
    question_id = db.Column(db.Integer, primary_key=True)  # Clave primaria
    question_text = db.Column(db.String(120), nullable=False)  # Obligatorio
    is_question_active = db.Column(db.Boolean, nullable=False)  # Obligatorio
