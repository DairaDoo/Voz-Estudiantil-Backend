from flask import Blueprint, jsonify, request
from app.models.professor_responses import ProfessorResponse

class ProfessorResponseRoutes:
    def __init__(self):
        self.blueprint = Blueprint('professor_response_routes', __name__)
        self._register_routes()

    def _register_routes(self):
        self.blueprint.add_url_rule(
            '/responses', view_func=self.create_response_route, methods=['POST']
        )
        self.blueprint.add_url_rule(
            '/responses/<int:response_id>', view_func=self.get_response_route, methods=['GET']
        )
        self.blueprint.add_url_rule(
            '/responses/<int:response_id>', view_func=self.update_response_route, methods=['PUT']
        )
        self.blueprint.add_url_rule(
            '/responses/<int:response_id>', view_func=self.delete_response_route, methods=['DELETE']
        )
        self.blueprint.add_url_rule(
            '/responses/all', view_func=self.get_all_responses_route, methods=['GET']
        )
        
        self.blueprint.add_url_rule(
            '/professors/average_response/<int:professor_id>', 
            view_func=self.get_average_response_route, 
            methods=['GET']
        )

    def create_response_route(self):
        try:
            data = request.get_json()
            user_id = data.get('user_id')
            professor_id = data.get('professor_id')
            question_id = data.get('question_id')
            answer = data.get('answer')
            state = data.get('state', 'pendiente')

            if not user_id or not professor_id or not question_id or answer is None:
                return jsonify({"error": "Los campos 'user_id', 'professor_id', 'question_id' y 'answer' son obligatorios."}), 400

            response = ProfessorResponse()
            response_id = response.create_response(user_id, professor_id, question_id, answer, state)

            return jsonify({"message": "Respuesta creada", "response_id": response_id}), 201
        except Exception as e:
            return jsonify({"error": "Error al crear la respuesta", "details": str(e)}), 500

    def get_response_route(self, response_id):
        try:
            response = ProfessorResponse()
            result = response.get_response(response_id)

            if not result:
                return jsonify({"error": "Respuesta no encontrada"}), 404

            return jsonify({"response": result}), 200
        except Exception as e:
            return jsonify({"error": "Error al obtener la respuesta", "details": str(e)}), 500

    def update_response_route(self, response_id):
        try:
            data = request.get_json()
            answer = data.get('answer')
            state = data.get('state')

            response = ProfessorResponse()
            updated_response = response.update_response(response_id, answer, state)

            if not updated_response:
                return jsonify({"error": "Respuesta no encontrada"}), 404

            return jsonify({"message": "Respuesta actualizada", "response": updated_response}), 200
        except Exception as e:
            return jsonify({"error": "Error al actualizar la respuesta", "details": str(e)}), 500

    def delete_response_route(self, response_id):
        try:
            response = ProfessorResponse()
            rows_deleted = response.delete_response(response_id)

            if rows_deleted == 0:
                return jsonify({"error": "Respuesta no encontrada"}), 404

            return jsonify({"message": "Respuesta eliminada"}), 200
        except Exception as e:
            return jsonify({"error": "Error al eliminar la respuesta", "details": str(e)}), 500

    def get_all_responses_route(self):
        try:
            response = ProfessorResponse()
            results = response.get_all_responses()

            if not results:
                return jsonify({"message": "No se encontraron respuestas"}), 404

            return jsonify({"responses": results}), 200
        except Exception as e:
            return jsonify({"error": "Error al obtener las respuestas", "details": str(e)}), 500
        
    def get_average_response_route(self, professor_id):
        """
        Devuelve el promedio de respuestas para un profesor específico.
        """
        try:
            professor_response = ProfessorResponse()
            average = professor_response.calculate_overall_rating(professor_id)

            if average is None:
                return jsonify({"message": "No hay respuestas registradas para este profesor."}), 404

            return jsonify({"professor_id": professor_id, "average_response": round(average, 2)}), 200

        except Exception as e:
            return jsonify({"error": "Error al obtener el promedio de respuestas", "details": str(e)}), 500

# Inicializar y exportar las rutas
professor_response_routes = ProfessorResponseRoutes().blueprint
