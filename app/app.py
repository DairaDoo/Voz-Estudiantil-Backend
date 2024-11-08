from flask import Flask
from config import Config
from flask_migrate import Migrate
from .utils import db

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

