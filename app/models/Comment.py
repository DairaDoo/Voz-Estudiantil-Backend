from utils import db

class Comment(db.Model):
    __tablename__ = 'Comment'
    
    comment_id = db.Column(db.Integer, unique=True, primary_key=True)  # Clave primaria
    review_id = db.Column(db.Integer, db.ForeignKey('Reviews.review_id'), unique=True, nullable=False)  # Obligatorio y único
    comment = db.Column(db.Text(100), nullable=False)  # Obligatorio
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'))

    review = db.relationship('Review', backref='comments', lazy=True) # Relacion de Tablas
    user = db.relationship('User', backref='comments', lazy=True) #Relacion de Tablas