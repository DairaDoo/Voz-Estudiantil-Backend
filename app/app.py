# app.py
from flask import Flask
from config import Config, TestingConfig
from flask_migrate import Migrate
from .utils.db import db
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def create_app(db_url=None, testing=False):
    app = Flask(__name__)

    # Configure app based on environment
    if testing:
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(Config)

    # Initialize database
    db.init_app(app)

    # Configure migration
    migrate = Migrate(app, db)
    
    # Ruta simple para verificar la conexión
    @app.route('/')
    def home():
        return "Hola Mundo (Ruta De Testing)"

    return app
