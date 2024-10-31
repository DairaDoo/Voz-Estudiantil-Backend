import datetime
from utils import db


class Event(db.Model):
    __tablename__ = 'Event'
    
    event_id = db.Column(db.Integer, primary_key=True, unique=True)  # Clave primaria
    event_title = db.Column(db.Varchar(120), unique=True, nullable=False)  # Obligatorio y unico
    description = db.Column(db.Text(100), nullable=False)  # Obligatorio
    create_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)  # Obligatorio
    up_vote = db.Column(db.Integer, nullable=True)  # Opcional
    user_id = db.Column(db.Integer(50), nullable=False)  #Referencia a la tabla user_id 
    university_id = db.Column(db.Integer(50),unique=True nullable=False) #Referencia a la tabla university_id
    state = db.Column(db.Varchar(50),nullable=False) #Estado de revision
    image_name = db.Column(db.Varchar(200), nullable=True) #No es obligatorio

    def __repr__(self):
        return f'<User {self.name}, Email: {self.email}>'