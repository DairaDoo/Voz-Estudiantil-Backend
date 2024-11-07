import datetime
from utils import db
from sqlalchemy import Enum


class Event(db.Model):
    __tablename__ = 'Event'
    
    event_id = db.Column(db.Integer, primary_key=True, unique=True)  # Clave primaria
    event_title = db.Column(db.String(120), nullable=False)  # Obligatorio, puede haber varios eventos con titulos iguales.
    description = db.Column(db.Text(100), nullable=False)  # Obligatorio
    create_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)  # Obligatorio
    up_vote = db.Column(db.Integer, nullable=True)  # Opcional
    user_id = db.Column(db.Integer(50), nullable=False)  #Referencia a la tabla user_id 
    university_id = db.Column(db.Integer, nullable=False) #Referencia a la tabla university_id, no unique ya que varios eventos pueden ser de la misma universidad.
    state = db.Column(Enum('pendiente', 'aprobado', 'rechazado', name='state_enum'), default='pendiente', nullable=False) # Obligatorio, Estado de revision
    image_name = db.Column(db.String(200), nullable=True) # No es obligatorio

    def __repr__(self):
        return f'<User {self.name}, Email: {self.email}>'