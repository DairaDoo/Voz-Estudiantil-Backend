import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://voz_estudiantil_user:XJq1zZcmlaoGd4Tumb5JeGAqQrrXuGUc@dpg-csnps7ggph6c73bj3cog-a.oregon-postgres.render.com/voz_estudiantil_db_hd1d'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

print("Database URI:", Config.SQLALCHEMY_DATABASE_URI)  # Verificar la URI de la base de datos
