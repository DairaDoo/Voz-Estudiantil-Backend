from flask import Blueprint, jsonify, request
from app.models.campus import get_campuses_by_university

class CampusRoutes:
    def __init__(self):
        self.blueprint = Blueprint('campus_routes', __name__)
        self._register_routes()

    def _register_routes(self):
        """Registra las rutas asociadas con los campuses."""
        self.blueprint.add_url_rule(
            '/campuses', view_func=self.get_campuses_route, methods=['GET']
        )


    def get_campuses_route(self):
        """
        Endpoint para obtener los nombres de los campus asociados a una universidad.
        """
        try:
            # Obtener el parámetro 'university_id' desde los query parameters de la URL
            university_id = request.args.get('university_id')

            if not university_id:
                return jsonify({"error": "El parámetro 'university_id' es obligatorio en la URL."}), 400

            try:
                university_id = int(university_id)
            except ValueError:
                return jsonify({"error": "El parámetro 'university_id' debe ser un número entero válido."}), 400

            # Llamar al modelo para obtener los campus
            campuses = get_campuses_by_university(university_id)
            return jsonify(campuses), 200

        except Exception as e:
            return jsonify({"error": "Error al obtener campuses", "details": str(e)}), 500

# Inicializar y exportar las rutas
campus_routes = CampusRoutes().blueprint
