from app.utils.db import db
from app.utils.enum_utils import state_enum  


class Comment(db.Model):
    __tablename__ = 'Comment'
    
    comment_id = db.Column(db.Integer, unique=True, primary_key=True)  # Clave primaria
    review_id = db.Column(db.Integer, db.ForeignKey('Reviews.review_id'), unique=True, nullable=False)  # Obligatorio y único
    comment = db.Column(db.Text(100), nullable=False)  # Obligatorio
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'))  # Relación con 'User'
    
    review_id = db.relationship('Review', backref='comments', lazy=True)  # Relación con 'Review'
    user_id = db.relationship('User', backref='comments', lazy=True)  # Relación con 'User'

def __repr__(self):
        return f"<Comment {self.id} - {self.state}>"