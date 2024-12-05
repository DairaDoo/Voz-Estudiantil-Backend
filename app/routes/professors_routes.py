from flask import Blueprint, jsonify, request
from app.models.professor import Professor

class ProfessorRoutes:
    def __init__(self):
        self.blueprint = Blueprint('professor_routes', __name__)
        self._register_routes()

    def _register_routes(self):
        self.blueprint.add_url_rule(
            '/professors', view_func=self.create_professor_route, methods=['POST']
        )
        self.blueprint.add_url_rule(
            '/professors/<int:professor_id>', view_func=self.get_professor_route, methods=['GET']
        )
        self.blueprint.add_url_rule(
            '/professors/<int:professor_id>', view_func=self.update_professor_route, methods=['PUT']
        )
        self.blueprint.add_url_rule(
            '/professors/<int:professor_id>', view_func=self.delete_professor_route, methods=['DELETE']
        )
        self.blueprint.add_url_rule(
            '/professors/all', view_func=self.get_all_professors_route, methods=['GET']
        )

    def create_professor_route(self):
        try:
            data = request.get_json()
            name = data.get('name')
            department_id = data.get('department_id')
            overall_rating = data.get('overall_rating')
            state = data.get('state', 'pendiente')

            if not name or not department_id or overall_rating is None:
                return jsonify({"error": "Los campos 'name', 'department_id' y 'overall_rating' son obligatorios."}), 400

            professor = Professor()
            professor_id = professor.create_professor(name, department_id, overall_rating, state)

            return jsonify({"message": "Profesor creado", "professor_id": professor_id}), 201

        except Exception as e:
            return jsonify({"error": "Error al crear el profesor", "details": str(e)}), 500

    def get_professor_route(self, professor_id):
        try:
            professor = Professor()
            result = professor.get_professor(professor_id)

            if not result:
                return jsonify({"error": "Profesor no encontrado"}), 404

            return jsonify({"professor": result}), 200

        except Exception as e:
            return jsonify({"error": "Error al obtener el profesor", "details": str(e)}), 500

    def update_professor_route(self, professor_id):
        try:
            data = request.get_json()
            name = data.get('name')
            department_id = data.get('department_id')
            overall_rating = data.get('overall_rating')
            state = data.get('state')

            professor = Professor()
            updated_professor = professor.update_professor(professor_id, name, department_id, overall_rating, state)

            if not updated_professor:
                return jsonify({"error": "Profesor no encontrado"}), 404

            return jsonify({"message": "Profesor actualizado", "professor": updated_professor}), 200

        except Exception as e:
            return jsonify({"error": "Error al actualizar el profesor", "details": str(e)}), 500

    def delete_professor_route(self, professor_id):
        try:
            professor = Professor()
            rows_deleted = professor.delete_professor(professor_id)

            if rows_deleted == 0:
                return jsonify({"error": "Profesor no encontrado"}), 404

            return jsonify({"message": "Profesor eliminado"}), 200

        except Exception as e:
            return jsonify({"error": "Error al eliminar el profesor", "details": str(e)}), 500

    def get_all_professors_route(self):
        """Endpoint para obtener todos los profesores con el nombre del departamento."""
        try:
            professor = Professor()
            results = professor.get_all_professors()

            if not results:
                return jsonify({"message": "No se encontraron profesores"}), 404

            return jsonify({"professors": results}), 200

        except Exception as e:
            return jsonify({"error": "Error al obtener los profesores", "details": str(e)}), 500

# Inicializar y exportar las rutas
professor_routes = ProfessorRoutes().blueprint
