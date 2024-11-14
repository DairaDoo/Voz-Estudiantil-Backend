from app.utils.db import db
from app.utils.enum_utils import state_enum  


class Campus(db.Model):
    __tablename__ = 'Campus'
    
    campus_id = db.Column(db.Integer, unique=True, primary_key=True)  # Clave primaria
    name = db.Column(db.String(50), db.ForeignKey('Universities.university_id'), unique=True, nullable=False)  # Obligatorio y único
    
    university_id = db.relationship('University', backref='campuses', lazy=True)  # Relación con 'University'

def __repr__(self):
        return f"<Campus {self.id} - {self.state}>"