from flask import Blueprint, request, jsonify
from app.models.user import create_user, verify_user_password
from app.schemas.user_schema import UserSchema, LoginSchema
from marshmallow import ValidationError
import bcrypt  # Importamos bcrypt para el hashing de contraseñas

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/users/create_user', methods=['POST'])
def create_user_route():
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

# Aquí van los otros endpoints
@user_routes.route('/users/rutafalsa', methods=['GET'])
def ruta_falsa():
    return jsonify(
        {
            "Saludo": "Hola Mundo!"
        }
    ), 400


@user_routes.route('/users/login', methods=['POST'])
def login_user_route():
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

    