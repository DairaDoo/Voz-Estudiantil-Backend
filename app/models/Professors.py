from app.utils.db import db
from utils.enum_utils import state_enum  
  # Importa el Enum

class Professors(db.Model):
    __tablename__ = 'Professors'
    
    professors_id = db.Column(db.Integer, primary_key=True)  # Clave primaria
    name = db.Column(db.String(50), nullable=False)  # Obligatorio, puede haber profesores con el mismo nombre.
    department_id = db.Column(db.Integer, db.ForeignKey('Departments.department_id'), nullable=False)  # Obligatorio
    overall_rating = db.Column(db.Float, nullable=False)  # Obligatorio
    state = db.Column(state_enum, default='pendiente', nullable=False)  # Estado de la revisión
    
    department = db.relationship('Department', backref='professors', lazy=True)  # Relación con 'Department'
