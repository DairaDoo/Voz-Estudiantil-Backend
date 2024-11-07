from utils import db

class University(db.Model):
    __tablename__ = 'University'
    
    university_id = db.Column(db.Integer, primary_key=True, unique=True)  # Clave primaria
    name = db.Column(db.String(50), unique=True, nullable=False)  # Obligatorio y único
    campus_id = db.Column(db.Integer, unique=True, nullable=False)  # Obligatorio y único

    # Relaciones (puedes agregar otras relaciones si es necesario, como con los 'Departments')
    campus = db.relationship('Campus', backref='university', lazy=True)
