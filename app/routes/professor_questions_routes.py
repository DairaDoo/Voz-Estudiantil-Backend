from flask import Blueprint, jsonify, request
from app.models.professor_questions import ProfessorQuestion

class ProfessorQuestionRoutes:
    def __init__(self):
        self.blueprint = Blueprint('professor_question_routes', __name__)
        self._register_routes()

    def _register_routes(self):
        self.blueprint.add_url_rule(
            '/professor_questions', view_func=self.get_all_questions_route, methods=['GET']
        )
        self.blueprint.add_url_rule(
            '/questions/<int:question_id>', view_func=self.get_question_route, methods=['GET']
        )

    def get_all_questions_route(self):
        try:
            professor_question = ProfessorQuestion()
            questions = professor_question.get_all_questions()

            if not questions:
                return jsonify({"message": "No se encontraron preguntas"}), 404

            return jsonify({"questions": questions}), 200
        except Exception as e:
            return jsonify({"error": "Error al obtener las preguntas", "details": str(e)}), 500

    def get_question_route(self, question_id):
        try:
            professor_question = ProfessorQuestion()
            result = professor_question.get_question_by_id(question_id)

            if not result:
                return jsonify({"error": "Pregunta no encontrada"}), 404

            return jsonify({"question": result}), 200
        except Exception as e:
            return jsonify({"error": "Error al obtener la pregunta", "details": str(e)}), 500

# Inicializar y exportar las rutas
professor_question_routes = ProfessorQuestionRoutes().blueprint
