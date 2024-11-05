from utils import db

class University(db.Model):
    __tablename__ = 'University'
    
    university_id = db.Column(db.Integer, primary_key=True)  # Clave primaria
    name = db.Column(db.Varchar(50), unique=True, nullable=False)  # Obligatorio y único
    campus_id = db.Column(db.Integer, unique=True, nullable=False)  # Obligatorio y unico
    