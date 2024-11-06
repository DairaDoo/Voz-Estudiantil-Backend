from utils import db

class Moderation(db.Model):
    __tablename__ = 'Moderation'
    
    moderation_id = db.Column(db.Integer,primary_key=True)  # Clave primaria
    item_id = db.Column(db.Integer)  
    tipo = db.Column(db.Varchar(100), nullable=False)  # Obligatorio
    password = db.Column(db.String(200), nullable=False)  # Obligatorio
    university_id = db.Column(db.Integer, nullable=True)  # Opcional
    rol = db.Column(db.String(50), nullable=False)  # Obligatorio