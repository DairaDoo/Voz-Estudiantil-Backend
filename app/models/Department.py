from utils import db


class Department(db.Model):
    __tablename__ = 'Department'
    
    department_id = db.Column(db.Integer, primary_key=True, unique=True)  # Clave primaria
    name = db.Column(db.Varchar(50), unique=True, nullable=False)  # Obligatorio y unico
    university_id = db.Column(db.Integer, nullable=False)  # Obligatorio