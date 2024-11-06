import datetime
from utils import db
from sqlalchemy import Enum # usamos esto para dar 3 posibles valores al state

class Professors_Responses(db.Model):
    __tablename__ = 'Professors_Responses'
    
    responses_id = db.Column(db.Integer, primary_key=True, unique=True)  # Clave primaria
    user_id = db.Column(db.Integer, nullable=False)  # Obligatorio, no es único por que un usario puede responder varias preguntas.
    professor_id = db.Column(db.Text(100), nullable=False)  # Obligatorio
    question_id = db.Column(db.Integer, nullable=False)  # Obligatorio
    anwser = db.Column(db.Integer, nullable=False)  # Obligatorio, debe haber siempre una respuesta de 1 a 5 estrellas.
    response_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)  # Obligatorio
    state = db.Column(Enum('pendiente', 'aprobado', 'rechazado', name='state_enum'), default='pendiente', nullable=False) # Obligatorio, Estado de revision
  