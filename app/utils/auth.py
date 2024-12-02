from flask import request, jsonify
import jwt

SECRET_KEY = "VozEstudiantil"

def token_required(f):
    """
    Decorador para rutas protegidas.
    """
    def decorator(*args, **kwargs):
        token = request.headers.get("Authorization")  # Leer el token del encabezado
        if not token:
            return jsonify({"error": "Token requerido"}), 401
        
        # Verificar si el token tiene el prefijo "Bearer"
        if not token.startswith("Bearer "):
            return jsonify({"error": "Formato de token inválido"}), 401
        
        try:
            # Eliminar el prefijo "Bearer " para obtener solo el token
            token = token.split(" ")[1]
            # Decodificar el token
            decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            # Agregar el user_id al contexto de la petición
            request.user_id = decoded.get("user_id")
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "El token ha expirado"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Token inválido"}), 401
        return f(*args, **kwargs)
    return decorator

