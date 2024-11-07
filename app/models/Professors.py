from utils import db
from sqlalchemy import Enum
class Professors(db.Model):
    __tablename__ = 'Professors'
    
    professors_id = db.Column(db.Integer, primary_key=True)  # Clave primaria
    name = db.Column(db.Varchar(50), nullable=False)  # Obligatorio, puede haber profesores con el mismo nombre.
    department_id = db.Column(db.Integer, db.ForeignKey('Departments.department_id'), nullable=False)  # Obligatorio
    overrall_rating = db.Column(db.Float, nullable=False)  # Obligatorio
    state = db.Column(Enum('pendiente', 'aprobado', 'rechazado', name='state_enum'), default='pendiente', nullable=False)  # Obligatorio
    
    department = db.relationship('Department', backref='professors', lazy=True) # Relacion de tablas