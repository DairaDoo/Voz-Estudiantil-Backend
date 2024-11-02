from utils import db

class Campus(db.Model):
    __tablename__ = 'Campus'
    
    campus_id = db.Column(db.Integer, unique=True, primary_key=True)  # Clave primaria
    name = db.Column(db.Varchar(50), unique=True, nullable=False)  # Obligatorio y único