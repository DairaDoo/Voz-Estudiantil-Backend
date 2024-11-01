import datetime
from utils import db

class Professors_Responses(db.Model):
    __tablename__ = 'Professors_Responses'
    
    responses_id = db.Column(db.Integer, primary_key=True, unique=True)  # Clave primaria
    user_id = db.Column(db.Integer, unique=True, nullable=False)  # Obligatorio y unico
    professor_id = db.Column(db.Text(100), nullable=False)  # Obligatorio
    question_id = db.Column(db.Integer, nullable=False)  # Obligatorio
    anwser = db.Column(db.Integer, nullable=True)  # Opcional
    response_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)  # Obligatorio
    state = db.Column(db.Varchar(50),nullable=False) #Estado de revision
  