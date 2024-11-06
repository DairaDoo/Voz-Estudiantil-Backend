import datetime
from utils import db
from sqlalchemy import Enum

class Moderation(db.Model):
    __tablename__ = 'Moderation'
    
    moderation_id = db.Column(db.Integer, unique=True, primary_key=True)  # Clave primaria
    related_content_id = db.Column(db.Integer) # Integer, se refiere al id del contenido (eventos, profesores o reseñas).
    content_type = db.Column(db.Varchar(100), nullable=False)  # Obligatorio, tipo contenido revisado (eventos, profesores o reseñas)
    state = db.Column(Enum('pendiente', 'aprobado', 'rechazado', name='state_enum'), default='pendiente', nullable=False)  # Estado de la petición
    rejection_reason = db.Column(db.Text(100), nullable=True) # Opcional, razón de rechazo.
    user_id = db.Column(db.Integer) # id del moderador (referencia a User).
    revision_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False) # día que se realizó la revsión, obligatoro.