from flask import Blueprint, request, jsonify
from app.models.user import create_user, verify_user_password
from app.schemas.user_schema import UserSchema, LoginSchema
from marshmallow import ValidationError
import bcrypt

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
            
            password = validated_data.get('password')
            if password:
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())  # Crear el hash de la contraseña
                validated_data['password'] = hashed_password.decode('utf-8')  # Reemplazar la contraseña con el hash

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
            # Obtener y validar los datos del cuerpo de la solicitud
            data = request.get_json()
            schema = LoginSchema()
            validated_data = schema.load(data)  # Validar datos
            
            email = validated_data['email']
            password = validated_data['password']

            # Verificar las credenciales del usuario
            user = verify_user_password(email, password)
            
            if user:
                # Si las credenciales son correctas, devolver una respuesta positiva
                return jsonify({"message": "Log in exitoso", "user_id": user['user_id'], "name": user['name']}), 200
            else:
                # Si las credenciales son incorrectas, devolver un error
                return jsonify({"error": "Credenciales incorrectas"}), 401

        except ValidationError as ve:
            # Manejar errores de validación
            return jsonify({"error": "Datos inválidos", "details": ve.messages}), 400
        except Exception as e:
            # Manejar errores internos del servidor
            return jsonify({"error": "Error interno del servidor", "details": str(e)}), 500

    def ruta_falsa(self):
        """
        Ejemplo de ruta adicional.
        """
        return jsonify({"Saludo": "Hola Mundo!"}), 400

# Inicializar y exportar las rutas
user_routes = UserRoutes().blueprint
