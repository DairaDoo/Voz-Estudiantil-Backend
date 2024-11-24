from flask import Flask
from config import Config
from app.routes.user_routes import user_routes  # Registra el Blueprint de las rutas de usuario
from app.routes.review_routes import review_routes
from flask_cors import CORS

# Inicializa la aplicación Flask
app = Flask(__name__)

# Habilitar CORS para todas las rutas
CORS(app)

# Configura la aplicación con variables del archivo de configuración
app.config.from_object(Config)

# Registrar el Blueprint de usuarios con el prefijo '/users'
app.register_blueprint(user_routes)
app.register_blueprint(review_routes)

# Inicia la aplicación
if __name__ == "__main__":
    app.run(debug=True)
