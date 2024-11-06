import datetime
from enum import Enum
from utils import db

class User(db.Model):
    __tablename__ = 'Users'
    
    # Definición del Enum inline en el campo rol
    class RoleEnum(Enum):
        usuario = "usuario"
        moderador = "moderador"
        administrador = "administrador"

    user_id = db.Column(db.Integer, primary_key=True)  # Clave primaria
    email = db.Column(db.String(120), unique=True, nullable=False)  # Obligatorio y único
    name = db.Column(db.String(100), nullable=False)  # Obligatorio
    password = db.Column(db.String(200), nullable=False)  # Obligatorio
    create_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)  # Obligatorio
    university_id = db.Column(db.Integer, db.ForeignKey('University.university_id'), nullable=True)  # Opcional y clave foránea
    rol = db.Column(db.Enum(RoleEnum), nullable=False, default=RoleEnum.usuario)  # Default a 'usuario', los moderadores y admin se crearán con SQL no en el register.
    
    def __repr__(self):
        return f'<User {self.name}, Email: {self.email}>'
