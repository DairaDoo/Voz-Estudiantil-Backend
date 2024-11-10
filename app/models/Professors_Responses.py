import datetime
from app.utils.db import db
from utils.enum_utils import state_enum  # Importa el Enum

class Professors_Responses(db.Model):
    __tablename__ = 'Professors_Responses'
    
    responses_id = db.Column(db.Integer, primary_key=True)  # Clave primaria
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)  # Clave foránea a Users
    professor_id = db.Column(db.Integer, db.ForeignKey('Professors.professors_id'), nullable=False)  # Clave foránea a Professors
    question_id = db.Column(db.Integer, db.ForeignKey('Professors_Questions.question_id'), nullable=False)  # Clave foránea a Professors_Questions
    answer = db.Column(db.Integer, nullable=False)  # Respuesta de 1 a 5 estrellas
    response_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)  # Obligatorio
    state = db.Column(state_enum, default='pendiente', nullable=False)  # Estado de la revisión

    # Relaciones
    user = db.relationship('User', backref='professors_responses', lazy=True)
    professor = db.relationship('Professors', backref='professors_responses', lazy=True)
    question = db.relationship('Professors_Questions', backref='professors_responses', lazy=True)
