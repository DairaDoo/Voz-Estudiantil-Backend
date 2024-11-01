import datetime
from utils import db


class Review(db.Model):
    __tablename__ = 'Review'
    
    review_id = db.Column(db.Integer, primary_key=True)  # Clave primaria
    review = db.Column(db.Text(120), unique=True, nullable=False)  # Obligatorio y unico
    user_id = db.Column(db.Integer(100), nullable=False)  # Obligatorio
    image_name = db.Column(db.Varchar(200), nullable=False)  # Obligatorio
    create_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)  # Obligatorio
    up_vote = db.Column(db.Integer, nullable=True)  # Opcional
    down_vote = db.Column(db.Integer(50), nullable=True)  # Obpcional
    university_id = db.Column(db.Integer,unique=True, nullable=False) # Obligatorio
    state = db.Column(db.Varchar(50),nullable=False)

