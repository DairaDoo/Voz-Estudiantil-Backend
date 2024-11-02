from utils import db

class Comment(db.Model):
    __tablename__ = 'Comment'
    
    comment_id = db.Column(db.Integer, unique=True, primary_key=True)  # Clave primaria
    review_id = db.Column(db.Integer, unique=True, nullable=False)  # Obligatorio y único
    comment = db.Column(db.Text(100), nullable=False)  # Obligatorio
    user_id = db.Column(db.Integer)  