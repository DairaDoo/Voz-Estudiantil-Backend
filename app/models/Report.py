from utils import db


class Report(db.Model):
    __tablename__ = 'Report'
    
    report_id = db.Column(db.Integer, primary_key=True, unique=True)  # Clave primaria
    user_id = db.Column(db.Integer, nullable=False)  # Obligatorio, Referencia a la tabla user_id 
    report_category_id = db.Column(db.Integer, nullable=False)  # Obligatorio, Referencia a la tabla report_category
    description = db.Column(db.String(100), nullable=True)  # Opcional
    review_id = db.Column(db.Integer, nullable=False)  # Obligatorio, Referencia a la tabla review