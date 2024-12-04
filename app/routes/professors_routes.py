from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app.models.professors import create_professor, get_professors
from app.schemas.professor import ProfessorSchema

professors_bp = Blueprint('professors', __name__)

# Instancia del esquema
professor_schema = ProfessorSchema()
professors_schema = ProfessorSchema(many=True)

@professors_bp.route('/professors', methods=['POST'])
def create_professor_route():
    """
    Ruta para crear un nuevo profesor.
    """
    try:
        # Validar y deserializar los datos de entrada
        data = professor_schema.load(request.get_json())
        
        # Crear el profesor
        result = create_professor(data)
        
        # Devolver la respuesta serializada
        return jsonify(result), 201
    except ValidationError as e:
        # Manejar errores de validación
        return jsonify({"error": e.messages}), 400
    except Exception as e:
        return jsonify({"error": f"Error del servidor: {str(e)}"}), 500


@professors_bp.route('/professors', methods=['GET'])
def get_professors_route():
    """
    Ruta para obtener todos los profesores.
    """
    try:
        professors = get_professors()
        
        # Serializar la respuesta con el esquema
        result = professors_schema.dump(professors)
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": f"Error del servidor: {str(e)}"}), 500
