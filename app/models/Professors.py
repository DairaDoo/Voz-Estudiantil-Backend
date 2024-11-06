from utils import db
from sqlalchemy import Enum
class Professors(db.Model):
    __tablename__ = 'Professors'
    
    professor_id = db.Column(db.Integer, primary_key=True, unique=True)  # Clave primaria
    name = db.Column(db.Varchar(50), nullable=False)  # Obligatorio, puede haber profesores con el mismo nombre.
    department_id = db.Column(db.Integer, nullable=False)  # Obligatorio
    overrall_rating = db.Column(db.Float, nullable=False)  # Obligatorio
    state = db.Column(Enum('pendiente', 'aprobado', 'rechazado', name='state_enum'), default='pendiente', nullable=False)  # Obligatorio