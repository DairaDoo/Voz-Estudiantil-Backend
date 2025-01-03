from flask import Blueprint, request, jsonify, current_app
from app.models.user import create_user, verify_user_password
from app.schemas.user_schema import UserSchema, LoginSchema
from marshmallow import ValidationError
import bcrypt
import jwt
from datetime import datetime, timedelta


class UserRoutes:
    def __init__(self):
        self.blueprint = Blueprint('user_routes', __name__)
        self._register_routes()

    def _register_routes(self):
        """Registra las rutas asociadas con los usuarios."""
        self.blueprint.add_url_rule('/users/create_user', view_func=self.create_user_route, methods=['POST'])
        self.blueprint.add_url_rule('/users/login', view_func=self.login_user_route, methods=['POST'])
        self.blueprint.add_url_rule('/users/rutafalsa', view_func=self.ruta_falsa, methods=['GET'])

    def create_user_route(self):
        """
        Endpoint para crear un usuario.
        """
        try:
            # Obtener los datos del cuerpo de la solicitud
            data = request.get_json()

            # Validar y deserializar los datos usando UserSchema
            schema = UserSchema()
            validated_data = schema.load(data)

            # Hash de la contraseña
            password = validated_data.get('password')
            if password:
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                validated_data['password'] = hashed_password.decode('utf-8')

            # Manejar university_id nulo
            university_id = validated_data.get('university_id')
            if not university_id:
                validated_data['university_id'] = None

            # Crear el usuario usando los datos validados
            result = create_user(validated_data)

            # Serializar la respuesta antes de enviarla
            return jsonify(schema.dump(result)), 201

        except ValueError as e:
            return jsonify({"error": str(e)}), 400

        except Exception as e:
            return jsonify({"error": "Error interno del servidor", "details": str(e)}), 500



    def login_user_route(self):
        """
        Endpoint para iniciar sesión de un usuario.
        """
        try:
            data = request.get_json()
            schema = LoginSchema()
            validated_data = schema.load(data)

            email = validated_data['email']
            password = validated_data['password']

            user = verify_user_password(email, password)

            if user:
                # Obtener SECRET_KEY desde la configuración de Flask
                secret_key = current_app.config["SECRET_KEY"]

                # Generar un token JWT
                payload = {
                    "user_id": user['user_id'],
                    "university_id": user.get('university_id'),  # Incluir university_id en el token
                    "exp": datetime.utcnow() + timedelta(hours=24)
                }
                token = jwt.encode(payload, secret_key, algorithm="HS256")

                return jsonify({
                    "message": "Log in exitoso",
                    "token": token,
                    "user_id": user['user_id'],
                    "name": user['name'],
                    "university_id": user.get('university_id')  # Incluir university_id en la respuesta JSON
                }), 200
            else:
                return jsonify({"error": "Credenciales incorrectas"}), 401

        except ValidationError as ve:
            return jsonify({"error": "Datos inválidos", "details": ve.messages}), 400
        except Exception as e:
            return jsonify({"error": "Error interno del servidor", "details": str(e)}), 500



    def ruta_falsa(self):
        """
        Ejemplo de ruta adicional.
        """
        return jsonify({"Saludo": "Hola Mundo!"}), 400

# Inicializar y exportar las rutas
user_routes = UserRoutes().blueprint
