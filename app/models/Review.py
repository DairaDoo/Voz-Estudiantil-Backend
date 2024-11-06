import datetime
from utils import db
from sqlalchemy import Enum


class Review(db.Model):
    __tablename__ = 'Review'
    
    review_id = db.Column(db.Integer, primary_key=True, unique=True)  # Clave primaria
    review = db.Column(db.Text(120), nullable=False)  # Obligatorio
    user_id = db.Column(db.Integer(100), nullable=False)  # Obligatorio
    image_name = db.Column(db.Varchar(200), nullable=True)  # Opcional
    create_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)  # Obligatorio
    up_vote = db.Column(db.Integer, nullable=True)  # Opcional
    down_vote = db.Column(db.Integer(50), nullable=True)  # Opcional
    university_id = db.Column(db.Integer, nullable=False) # Obligatorio
    state = db.Column(Enum('pendiente', 'aprobado', 'rechazado', name='state_enum'), default='pendiente', nullable=False)  # Obligatorio

