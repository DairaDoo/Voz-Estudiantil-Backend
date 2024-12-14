from flask import Blueprint, request, jsonify
from app.models.comments import CommentModel
from app.schemas.comment_schema import CommentSchema, CommentWithUserSchema
from marshmallow import ValidationError

from app.utils.auth import token_required

class CommentRoutes:
    def __init__(self):
        self.blueprint = Blueprint('comment_routes', __name__)
        self.model = CommentModel()
        self.schema = CommentSchema()
        self.user_schema = CommentWithUserSchema(many=True)
        self._register_routes()

    def _register_routes(self):
        self.blueprint.add_url_rule('/comments', view_func=self.get_all_comments_route, methods=['GET'])
        self.blueprint.add_url_rule('/comments', view_func=self.create_comment_route, methods=['POST'])
        self.blueprint.add_url_rule('/comments-with-usernames', view_func=self.get_all_comments_with_usernames_route, methods=['GET'])
        self.blueprint.add_url_rule('/comments-by-review', view_func=self.get_comments_by_review_route, methods=['GET'])

    @token_required
    def create_comment_route(self):
        """
        Crea un nuevo comentario con validación.
        """
        try:
            data = request.get_json()
            validated_data = self.schema.load(data)  # Validación de datos
            comment_id = self.model.create_comment(validated_data)  # Creación del comentario
            return jsonify({"message": "Comentario creado", "comment_id": comment_id}), 201
        except ValidationError as ve:
            return jsonify({"error": "Datos inválidos", "details": ve.messages}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def get_all_comments_route(self):
        """
        Obtiene todos los comentarios registrados.
        """
        try:
            comments = self.model.get_all_comments()
            result = self.schema.dump(comments, many=True)  # Serializa la salida
            return jsonify(result), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def get_all_comments_with_usernames_route(self):
        """
        Devuelve todos los comentarios con el nombre del usuario que los realizó, en vez de user_id.
        """
        try:
            comments = self.model.get_all_comments_with_usernames()  # Consulta que incluye el user_name
            result = self.user_schema.dump(comments, many=True)  # Serializa la salida con nombre de usuario
            return jsonify(result), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def get_comments_by_review_route(self):
        """
        Devuelve todos los comentarios asociados a un 'review_id' específico.
        """
        try:
            review_id = request.args.get('review_id', type=int)  # Obtener review_id desde los parámetros de la URL
            if not review_id:
                return jsonify({"error": "El parámetro 'review_id' es obligatorio."}), 400
            
            comments = self.model.get_comments_by_review(review_id)
            result = self.user_schema.dump(comments)  # Serializa la salida con nombre de usuario
            return jsonify(result), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

# Inicializar y exportar las rutas
comment_routes = CommentRoutes().blueprint
