from utils import db

class Campus(db.Model):
    __tablename__ = 'Campus'
    campus_id = db.Column(db.Integer, unique=True, primary_key=True)  # Clave primaria
    name = db.Column(db.Varchar(50), db.ForeignKey('Universities.university_id'), unique=True, nullable=False)  # Obligatorio y único
    
    university = db.relationship('University', backref='campuses', lazy=True) # Relacion de tablas
