from utils import db
class Department(db.Model):
    __tablename__ = 'Department'
    
    department_id = db.Column(db.Integer, unique=True, primary_key=True)  # Clave primaria
    name = db.Column(db.String(50), unique=True, nullable=False)  # Obligatorio y único
    university_id = db.Column(db.Integer, db.ForeignKey('Universities.university_id'), nullable=False)  # Obligatorio
    
    university_id = db.relationship('University', backref='departments', lazy=True)  # Relación con 'University'
