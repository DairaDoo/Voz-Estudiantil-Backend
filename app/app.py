from flask import Flask, jsonify

import datetime

def create_app():
    app = Flask(__name__)

    
    # Ruta simple que retorna un mensaje
    @app.route('/')
    def home():
        return "Hola Mundo ( Ruta De Testing )"
    
    
        
    
    return app
