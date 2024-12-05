from flask import Blueprint, jsonify, request
from app.models.department import (
    get_all_departments,
    get_department_by_id,
    create_department,
    update_department,
    delete_department
)
from app.schemas.department_schema import DepartmentSchema


class DepartmentRoutes:
    def __init__(self):
        self.blueprint = Blueprint('department_routes', __name__)
        self._register_routes()

    def _register_routes(self):
        """Registra las rutas asociadas con los departamentos."""
        self.blueprint.add_url_rule(
            '/departments', view_func=self.get_departments_route, methods=['GET']
        )
        self.blueprint.add_url_rule(
            '/departments/<int:department_id>', view_func=self.get_department_by_id_route, methods=['GET']
        )
        self.blueprint.add_url_rule(
            '/departments', view_func=self.create_department_route, methods=['POST']
        )
        self.blueprint.add_url_rule(
            '/departments/<int:department_id>', view_func=self.update_department_route, methods=['PUT']
        )
        self.blueprint.add_url_rule(
            '/departments/<int:department_id>', view_func=self.delete_department_route, methods=['DELETE']
        )

    def get_departments_route(self):
        """
        Endpoint para obtener todos los departamentos.
        """
        try:
            departments = get_all_departments()
            schema = DepartmentSchema(many=True)
            return jsonify(schema.dump(departments)), 200
        except Exception as e:
            return jsonify({"error": "Error al obtener departamentos", "details": str(e)}), 500

    def get_department_by_id_route(self, department_id):
        """
        Endpoint para obtener un departamento por su ID.
        """
        try:
            department = get_department_by_id(department_id)
            if not department:
                return jsonify({"error": "Departamento no encontrado"}), 404
            schema = DepartmentSchema()
            return jsonify(schema.dump(department)), 200
        except Exception as e:
            return jsonify({"error": "Error al obtener el departamento", "details": str(e)}), 500

    def create_department_route(self):
        """
        Endpoint para crear un nuevo departamento.
        """
        try:
            data = request.get_json()
            department_id = data.get('department_id')
            name = data.get('name')
            university_id = data.get('university_id')

            if not department_id or not name or not university_id:
                return jsonify({"error": "Faltan datos requeridos"}), 400

            new_department = create_department(department_id, name, university_id)
            return jsonify(new_department), 201
        except Exception as e:
            return jsonify({"error": "Error al crear el departamento", "details": str(e)}), 500

    def update_department_route(self, department_id):
        """
        Endpoint para actualizar un departamento.
        """
        try:
            data = request.get_json()
            name = data.get('name')
            university_id = data.get('university_id')

            if not name and not university_id:
                return jsonify({"error": "No se proporcionaron datos para actualizar"}), 400

            updated_department = update_department(department_id, name=name, university_id=university_id)
            if "message" in updated_department and updated_department["message"] == "Departamento no encontrado":
                return jsonify(updated_department), 404

            return jsonify(updated_department), 200
        except Exception as e:
            return jsonify({"error": "Error al actualizar el departamento", "details": str(e)}), 500

    def delete_department_route(self, department_id):
        """
        Endpoint para eliminar un departamento.
        """
        try:
            deleted_department = delete_department(department_id)
            if "message" in deleted_department and deleted_department["message"] == "Departamento no encontrado":
                return jsonify(deleted_department), 404

            return jsonify(deleted_department), 200
        except Exception as e:
            return jsonify({"error": "Error al eliminar el departamento", "details": str(e)}), 500


# Inicializar y exportar las rutas
department_routes = DepartmentRoutes().blueprint
