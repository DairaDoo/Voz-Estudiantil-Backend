from flask import Blueprint, jsonify, request
import cloudinary.uploader
import os
import datetime
from app.models.events import EventModel
from app.utils.auth import token_required  # Asegúrate de tener este decorador si es necesario

class EventRoutes:
    def __init__(self):
        self.blueprint = Blueprint('event_routes', __name__)
        self.model = EventModel()
        self._register_routes()

    def _register_routes(self):
        self.blueprint.add_url_rule('/events', view_func=self.get_all_events_route, methods=['GET'])
        self.blueprint.add_url_rule('/events/<int:event_id>', view_func=self.get_event_route, methods=['GET'])
        self.blueprint.add_url_rule('/events', view_func=self.create_event_route, methods=['POST'])
        self.blueprint.add_url_rule('/events/<int:event_id>', view_func=self.update_event_route, methods=['PUT'])
        self.blueprint.add_url_rule('/events/<int:event_id>', view_func=self.delete_event_route, methods=['DELETE'])

    def _upload_image_to_cloudinary(self, image_file):
        """
        Sube una imagen a Cloudinary y devuelve el nombre o identificador único.
        """
        try:
            response = cloudinary.uploader.upload(
                image_file,
                folder=os.getenv("CLOUDINARY_UPLOAD_FOLDER", "events")
            )
            return response.get("public_id")  # Guardar solo el identificador
        except Exception as e:
            raise Exception(f"Error al subir la imagen: {e}")

    def get_all_events_route(self):
        """
        Obtiene todos los eventos.
        """
        try:
            events = self.model.get_all_events()
            return jsonify(events), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def get_event_route(self, event_id):
        """
        Obtiene un evento por su ID.
        """
        try:
            event = self.model.get_event(event_id)
            if not event:
                return jsonify({"error": "Evento no encontrado"}), 404
            return jsonify(event), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def create_event_route(self):
        """
        Crea un nuevo evento con validación manual y subida de imagen.
        """
        try:
            # Obtener datos enviados
            data = request.form.to_dict()
            
            # Validación simple de los datos del evento
            if not data.get('title') or not data.get('date') or not data.get('description') or not data.get('user_id') or not data.get('university_id'):
                return jsonify({"error": "Faltan campos obligatorios: 'title', 'date', 'description', 'user_id', 'university_id'"}), 400

            # Manejar subida de imagen si se envía
            if 'image' in request.files:
                image_file = request.files['image']
                image_name = self._upload_image_to_cloudinary(image_file)
            else:
                image_name = None

            # Establecer valores predeterminados
            event_data = {
                'title': data['title'],
                'description': data['description'],
                'user_id': data['user_id'],
                'university_id': data['university_id'],
                'image_name': image_name
            }

            # Crear evento en la base de datos
            new_event = self.model.create_event(event_data)
            return jsonify({"message": new_event["message"], "event_id": new_event["event_id"]}), 201

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def update_event_route(self, event_id):
        """
        Actualiza un evento existente con validación manual y subida de imagen.
        """
        try:
            data = request.get_json()

            # Validación simple
            if not data.get('title') or not data.get('date'):
                return jsonify({"error": "Faltan campos obligatorios: 'title' y 'date'"}), 400

            # Manejar subida de imagen si se envía
            if 'image' in request.files:
                image_file = request.files['image']
                image_name = self._upload_image_to_cloudinary(image_file)
                data['image_name'] = image_name

            # Actualizar el evento
            self.model.update_event(event_id, data)
            return jsonify({"message": "Evento actualizado"}), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def delete_event_route(self, event_id):
        """
        Elimina un evento por su ID.
        """
        try:
            self.model.delete_event(event_id)
            return jsonify({"message": "Evento eliminado"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500


# Inicializar y exportar las rutas
event_routes = EventRoutes().blueprint
