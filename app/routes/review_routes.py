from flask import Blueprint, request, jsonify
from app.models.review import ReviewModel
from marshmallow import ValidationError
from app.schemas.review_schema import ReviewSchema

class ReviewRoutes:
    def __init__(self):
        self.blueprint = Blueprint('review_routes', __name__)
        self.model = ReviewModel()
        self._register_routes()

    def _register_routes(self):
        self.blueprint.add_url_rule('/reviews/<int:review_id>', view_func=self.get_review_route, methods=['GET'])
        self.blueprint.add_url_rule('/reviews', view_func=self.create_review_route, methods=['POST'])
        self.blueprint.add_url_rule('/reviews/<int:review_id>', view_func=self.update_review_route, methods=['PUT'])
        self.blueprint.add_url_rule('/reviews/<int:review_id>', view_func=self.delete_review_route, methods=['DELETE'])

    def get_review_route(self, review_id):
        """
        Obtiene una reseña por su ID.
        """
        try:
            review = self.model.get_review(review_id)
            if not review:
                return jsonify({"error": "Reseña no encontrada"}), 404
            return jsonify(review), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def create_review_route(self):
        """
        Crea una nueva reseña.
        """
        try:
            data = request.get_json()
            schema = ReviewSchema()
            validated_data = schema.load(data)
            new_review_id = self.model.create_review(validated_data)
            return jsonify({"message": "Reseña creada", "review_id": new_review_id}), 201
        except ValidationError as ve:
            return jsonify({"error": "Datos inválidos", "details": ve.messages}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def update_review_route(self, review_id):
        """
        Actualiza una reseña existente.
        """
        try:
            data = request.get_json()
            schema = ReviewSchema()
            validated_data = schema.load(data)
            self.model.update_review(review_id, validated_data)
            return jsonify({"message": "Reseña actualizada"}), 200
        except ValidationError as ve:
            return jsonify({"error": "Datos inválidos", "details": ve.messages}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def delete_review_route(self, review_id):
        """
        Elimina una reseña.
        """
        try:
            self.model.delete_review(review_id)
            return jsonify({"message": "Reseña eliminada"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

# Inicializar y exportar las rutas
review_routes = ReviewRoutes().blueprint
