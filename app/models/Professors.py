from utils import db

class Professors(db.Model):
    __tablename__ = 'Professors'
    
    professors_id = db.Column(db.Integer, primary_key=True)  # Clave primaria
    name = db.Column(db.Varchar(50), unique=True, nullable=False)  # Obligatorio y único
    department_id = db.Column(db.Integer, db.ForeignKey('Departments.department_id'), nullable=False)  # Obligatorio
    overrall_rating = db.Column(db.Float, nullable=False)  # Obligatorio
    state = db.Column(db.Varchar(50), nullable=True)  # Opcional

    department = db.relationship('Department', backref='professors', lazy=True) # Relacion de tablas