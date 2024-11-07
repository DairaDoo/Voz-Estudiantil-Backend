import datetime
from utils import db
from utils.enum_utils import state_enum  # Importa el Enum

class Review(db.Model):
    __tablename__ = 'Review'
    
    review_id = db.Column(db.Integer, primary_key=True, unique=True)  # Clave primaria
    review = db.Column(db.Text(120), nullable=False)  # Obligatorio
    user_id = db.Column(db.Integer, nullable=False)  # Obligatorio
    image_name = db.Column(db.String(200), nullable=True)  # Opcional
    create_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)  # Obligatorio
    up_vote = db.Column(db.Integer, nullable=True)  # Opcional
    down_vote = db.Column(db.Integer, nullable=True)  # Opcional
    university_id = db.Column(db.Integer, db.ForeignKey('University.university_id'), nullable=False)  # Clave foránea a University
    state = db.Column(state_enum, default='pendiente', nullable=False)  # Estado de la revisión


    # Relaciones
    user = db.relationship('User', backref='reviews', lazy=True)
    university = db.relationship('University', backref='reviews', lazy=True)

    def __repr__(self):
        return f'<Review {self.review_id}, User {self.user_id}, University {self.university_id}>'
