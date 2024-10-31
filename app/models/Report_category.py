from utils import db


class Event(db.Model):
    __tablename__ = 'Event'
    
    report_category_id = db.Column(db.Integer, primary_key=True, unique=True)  # Clave primaria
    category_name = db.Column(db.Varchar(120), unique=True, nullable=False)  # Obligatorio y unico

    def __repr__(self):
        return f'<User {self.name}, Email: {self.email}>'