from flask import Blueprint
from controllers.questions import get_all_questions

# Crear el Blueprint para las rutas de preguntas
question_routes = Blueprint('question_routes', __name__)

# Ruta para obtener todas las preguntas
question_routes.route('/questions', methods=['GET'])(get_all_questions)
