from flask import Blueprint, request, jsonify
from app.models.user import create_user
from app.schemas.user_schema import UserSchema
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
