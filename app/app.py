from flask import Flask
from config import Config
from flask_migrate import Migrate
from .utils.db import db  # Correcta referencia de importación # Asegúrate de que utils.py contiene la instancia de db de SQLAlchemy
from app.models import Campus, Department, Event, Moderation, Professors_Questions, Professors_Responses, Report_category, Report, Professors, Review, University, User



def create_app():
    app = Flask(__name__)
    
    # Carga la configuración de la base de datos desde Config
    app.config.from_object(Config)
    
    # Inicializa la base de datos con la aplicación
    db.init_app(app)
    
    # Configura la migración
    migrate = Migrate(app, db)
    
    # Ruta simple para verificar la conexión
    @app.route('/')
    def home():
        return "Hola Mundo (Ruta De Testing)"
    
    return app

