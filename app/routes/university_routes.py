from flask import Blueprint, jsonify
from app.models.university import get_all_universities
from app.schemas.university_schema import UniversitySchema

class UniversityRoutes:
    def __init__(self):
        self.blueprint = Blueprint('university_routes', __name__)
        self._register_routes()

    def _register_routes(self):
        """Registra las rutas asociadas con las universidades."""
        self.blueprint.add_url_rule(
            '/universities', view_func=self.get_universities_route, methods=['GET']
        )

    def get_universities_route(self):
        """
        Endpoint para obtener todas las universidades.
        """
        try:
            # Obtener datos del modelo
            universities = get_all_universities()
            schema = UniversitySchema(many=True)
            return jsonify(schema.dump(universities)), 200

        except Exception as e:
            return jsonify({"error": "Error al obtener universidades", "details": str(e)}), 500

# Inicializar y exportar las rutas
university_routes = UniversityRoutes().blueprint
