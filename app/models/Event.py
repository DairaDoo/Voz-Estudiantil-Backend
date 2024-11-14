import datetime
from app.utils.db import db
from utils.enum_utils import state_enum  
  # Importa el Enum

class Event(db.Model):
    __tablename__ = 'Event'
    
    event_id = db.Column(db.Integer, primary_key=True, unique=True)  # Clave primaria
    event_title = db.Column(db.String(120), nullable=False)  # Obligatorio
    description = db.Column(db.Text, nullable=False)  # Obligatorio
    create_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)  # Obligatorio
    up_vote = db.Column(db.Integer, nullable=True)  # Opcional
    user_id = db.Column(db.Integer, nullable=False)  # Referencia a la tabla User
    university_id = db.Column(db.Integer, nullable=False)  # Referencia a la tabla University
    state = db.Column(state_enum, default='pendiente', nullable=False)  # Estado de la revisión
    image_name = db.Column(db.String(200), nullable=True)  # Opcional

    # Relaciones
    user = db.relationship('User', backref='events', lazy=True)
