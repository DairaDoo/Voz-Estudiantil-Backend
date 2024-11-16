from flask import Blueprint, request, jsonify
from app.models.user import create_user

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/users/create_user', methods=['POST'])
def create_user_route():
    """
    Endpoint para crear un usuario.
    """
    try:
        data = request.get_json()
        result = create_user(data)
        return jsonify(result), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "details": str(e)}), 500

# aquí van los otros endpoint
@user_routes.route('/users/rutafalsa', methods=['GET'])
def ruta_falsa():
    return jsonify(
        {
            "Saludo": "Hola Mundo!"
        }
    ), 400