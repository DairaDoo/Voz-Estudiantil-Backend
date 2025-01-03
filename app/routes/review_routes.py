from flask import Blueprint, request, jsonify
from app.models.review import ReviewModel
from app.schemas.review_schema import ReviewSchema
from marshmallow import ValidationError
import cloudinary.uploader
import os
import datetime
from app.utils.auth import token_required


class ReviewRoutes:
    def __init__(self):
        self.blueprint = Blueprint('review_routes', __name__)
        self.model = ReviewModel()
        self.schema = ReviewSchema()
        self._register_routes()

    def _register_routes(self):
        self.blueprint.add_url_rule('/reviews', view_func=self.get_all_reviews_route, methods=['GET'])
        self.blueprint.add_url_rule('/reviews/<int:review_id>', view_func=self.get_review_route, methods=['GET'])
        self.blueprint.add_url_rule('/reviews', view_func=self.create_review_route, methods=['POST'])
        self.blueprint.add_url_rule('/reviews/<int:review_id>', view_func=self.update_review_route, methods=['PUT'])
        self.blueprint.add_url_rule('/reviews/<int:review_id>', view_func=self.delete_review_route, methods=['DELETE'])
        self.blueprint.add_url_rule('/reviews_with_names', view_func=self.get_reviews_with_names_route, methods=['GET'])
        self.blueprint.add_url_rule( '/reviews/<int:review_id>/votes', view_func=self.update_review_votes_route,methods=['PUT'])
        self.blueprint.add_url_rule('/reviews/<int:review_id>/votes', view_func=self.get_review_votes_route,methods=['GET'])
    

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
        
        
    def get_all_reviews_route(self):
        """
        Obtiene todas las reseñas.
        """
        try:
            reviews = self.model.get_all_reviews()
            return jsonify(reviews), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    def get_reviews_with_names_route(self):
        """
        Obtiene todas las reseñas con los nombres de las universidades y usuarios.
        """
        try:
            reviews = self.model.get_all_reviews_with_names()  # Asegúrate de tener este método en ReviewModel
            return jsonify(reviews), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500



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
            
            # Validación de datos
            validated_data = self.schema.load(data)

            # Manejar subida de imagen si se envía
            if 'image' in request.files:
                image_file = request.files['image']
                validated_data['image_name'] = self._upload_image_to_cloudinary(image_file)
            else:
                validated_data['image_name'] = None

            # Establecer valores predeterminados
            validated_data['create_date'] = datetime.datetime.utcnow()

            # Si no se ha pasado un campus_id, se establece como None
            validated_data['campus_id'] = data.get('campus_id', None)

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

            # Si el campus es proporcionado, actualizarlo
            if 'campus_id' in data:
                validated_data['campus_id'] = data['campus_id']

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
        
    
    @token_required
    def update_review_votes_route(self, review_id):
        """
        Actualiza los votos de una reseña (up_vote o down_vote).
        """
        try:
            data = request.get_json()
            vote_type = data.get('type')

            if vote_type not in ['up', 'down']:
                return jsonify({"error": "Tipo de voto inválido"}), 400

            # Registra información útil para depurar
            print(f"User ID: {request.user_id} está votando '{vote_type}' en la reseña {review_id}")

            self.model.update_votes(review_id, vote_type)
            return jsonify({"message": f"{vote_type}_vote actualizado correctamente"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500


        
    def get_review_votes_route(self, review_id):
        """
        Obtiene el total de votos netos (up_vote - down_vote) de una reseña.
        """
        try:
            votes = self.model.get_total_votes(review_id)
            if votes is None:
                return jsonify({"error": "Reseña no encontrada"}), 404

            return jsonify({"total_votes": votes}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500



# Inicializar y exportar las rutas
review_routes = ReviewRoutes().blueprint
