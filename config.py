import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://voz_estudiantil_db_user:egsVv9dWWVJVhj4GxiXfth5kElhQ0TPe@dpg-csmfeb56l47c73eqvvd0-a/voz_estudiantil_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    