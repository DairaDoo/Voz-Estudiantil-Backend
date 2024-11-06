from utils import db


class Report_category(db.Model):
    __tablename__ = 'Report_category'
    
    report_category_id = db.Column(db.Integer, primary_key=True)  # Clave primaria
    category_name = db.Column(db.Varchar(120), unique=True, nullable=False)  # Obligatorio y unico