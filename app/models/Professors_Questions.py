import datetime
from utils import db

class Professors_Questions(db.Model):
    __tablename__ = 'Professors_Questions'
    
    question_id = db.Column(db.Integer, primary_key=True )  # Clave primaria
    question_text = db.Column(db.Varchar(120), nullable=False)  # Obligatorio y único
    is_question_active = db.Column(db.Bool, nullable=False)  # Obligatorio