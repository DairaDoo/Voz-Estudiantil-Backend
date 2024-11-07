from flask import Flask, jsonify
from utils import db
from config import Config
import datetime


def create_app():
    app = Flask(__name__)
    
    # Carga la configuración
    app.config.from_object(Config)

    # Inicializa la base de datos con la aplicación
    db.init_app(app)
    
    # Ruta simple para verificar la conexión
    @app.route('/')
    def home():
        return "Hola Mundo (Ruta De Testing)"
    
    # Crea todas las tablas en la base de datos si no existen
    with app.app_context():
        db.create_all()

    return app
