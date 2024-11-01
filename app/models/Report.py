from utils import db


class Report(db.Model):
    __tablename__ = 'Report'
    
    report_id = db.Column(db.Integer, primary_key=True, unique=True)  # Clave primaria
    user_id = db.Column(db.Integer(50), nullable=False)  #Referencia a la tabla user_id 
    report_category_id = db.Column(db.Integer, unique=True)  # Referencia a la tabla report_category
    description = db.Column(db.Varchar(100), nullable=False)  # Obligatorio
    review_id = db.Column(db.Integer)  # Referencia a la tabla review