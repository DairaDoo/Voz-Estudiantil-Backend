import datetime
from app.utils.db import db
from utils.enum_utils import state_enum  # Importa el Enum

class Moderation(db.Model):
    __tablename__ = 'Moderation'
    
    moderation_id = db.Column(db.Integer, unique=True, primary_key=True)  # Clave primaria
    related_content_id = db.Column(db.Integer)  # Se refiere al id del contenido (eventos, profesores, reseñas)
    content_type = db.Column(db.String(100), nullable=False)  # Obligatorio, tipo de contenido
    state = db.Column(state_enum, default='pendiente', nullable=False)  # Estado de la revisión
    rejection_reason = db.Column(db.Text, nullable=True)  # Opcional, razón de rechazo
    user_id = db.Column(db.Integer)  # ID del moderador
    revision_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)  # Fecha de la revisión

    # Relaciones
    user = db.relationship('User', backref='moderations', lazy=True)
