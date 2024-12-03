from flask import Blueprint, request, jsonify
from app.models.review import ReviewModel
from app.schemas.review_schema import ReviewSchema
from marshmallow import ValidationError
import cloudinary.uploader
import os
import datetime


class ReviewRoutes:
    def __init__(self):
        self.blueprint = Blueprint('review_routes', __name__)
        self.model = ReviewModel()
        self.schema = ReviewSchema()
        self._register_routes()

    def _register_routes(self):
        self.blueprint.add_url_rule('/reviews/<int:review_id>', view_func=self.get_review_route, methods=['GET'])
        self.blueprint.add_url_rule('/reviews', view_func=self.create_review_route, methods=['POST'])
        self.blueprint.add_url_rule('/reviews/<int:review_id>', view_func=self.update_review_route, methods=['PUT'])
        self.blueprint.add_url_rule('/reviews/<int:review_id>', view_func=self.delete_review_route, methods=['DELETE'])

    def _upload_image_to_cloudinary(self, image_file):
        """
        Sube una imagen a Cloudinary y devuelve el nombre o identificador único.
        """
        try:
            response = cloudinary.uploader.upload(
                image_file,
                folder=os.getenv("CLOUDINARY_UPLOAD_FOLDER", "reviews")
            )
            return response.get("public_id")  # Guardar solo el identificador
        except Exception as e:
            raise Exception(f"Error al subir la imagen: {e}")

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
        Crea una nueva reseña con validación del esquema y subida de imagen.
        """
        try:
            # Obtener datos enviados
            data = request.form.to_dict()
            validated_data = self.schema.load(data)

            # Manejar subida de imagen si se envía
            if 'image' in request.files:
                image_file = request.files['image']
                validated_data['image_name'] = self._upload_image_to_cloudinary(image_file)
            else:
                validated_data['image_name'] = None

            # Establecer valores predeterminados
            validated_data['create_date'] = datetime.datetime.utcnow()

            # Crear reseña en la base de datos
            new_review_id = self.model.create_review(validated_data)
            return jsonify({"message": "Reseña creada", "review_id": new_review_id}), 201

        except ValidationError as ve:
            return jsonify({"error": "Datos inválidos", "details": ve.messages}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def update_review_route(self, review_id):
        """
        Actualiza una reseña existente con validación del esquema.
        """
        try:
            data = request.get_json()
            validated_data = self.schema.load(data, partial=True)  # `partial=True` permite actualizar solo algunos campos

            # Manejar subida de imagen si se envía
            if 'image' in request.files:
                image_file = request.files['image']
                validated_data['image_name'] = self._upload_image_to_cloudinary(image_file)

            self.model.update_review(review_id, validated_data)
            return jsonify({"message": "Reseña actualizada"}), 200

        except ValidationError as ve:
            return jsonify({"error": "Datos inválidos", "details": ve.messages}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def delete_review_route(self, review_id):
        """
        Elimina una reseña por su ID.
        """
        try:
            self.model.delete_review(review_id)
            return jsonify({"message": "Reseña eliminada"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500


# Inicializar y exportar las rutas
review_routes = ReviewRoutes().blueprint
