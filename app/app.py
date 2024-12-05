from flask import Flask
from config import Config
from app.routes.user_routes import user_routes  # Registra el Blueprint de las rutas de usuario
from app.routes.review_routes import review_routes
from app.routes.university_routes import university_routes
from app.routes.campus_routes import campus_routes
from app.routes.professors_routes import professor_routes  # Agregar la importación de profesor
from app.routes.department_route import department_routes
from flask_cors import CORS
import cloudinary

# Inicializa la aplicación Flask
app = Flask(__name__)

# Habilitar CORS para todas las rutas
CORS(app)

# Configura la aplicación con variables del archivo de configuración
app.config.from_object(Config)


# Registrar los Blueprints
app.register_blueprint(user_routes)
app.register_blueprint(review_routes)
app.register_blueprint(university_routes)
app.register_blueprint(campus_routes)
app.register_blueprint(department_routes)
app.register_blueprint(professor_routes)  # Registra el Blueprint de los profesores

# Inicia la aplicación
if __name__ == "__main__":
    app.run(debug=True)
