import datetime
from utils import db

class User(db.Model):
    __tablename__ = 'Users'
    
    user_id = db.Column(db.Integer, primary_key=True)  # Clave primaria
    email = db.Column(db.String(120), unique=True, nullable=False)  # Obligatorio y único
    name = db.Column(db.String(100), nullable=False)  # Obligatorio
    password = db.Column(db.String(200), nullable=False)  # Obligatorio
    create_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)  # Obligatorio
    university_id = db.Column(db.Integer, nullable=True)  # Opcional
    rol = db.Column(db.String(50), nullable=False)  # Obligatorio
    
    def __repr__(self):
        return f'<User {self.name}, Email: {self.email}>'