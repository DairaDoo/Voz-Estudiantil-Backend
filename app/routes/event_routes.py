from flask import Blueprint, request, jsonify
from app.models.events import EventModel
from app.schemas.event_schema import EventSchema
from marshmallow import ValidationError
import cloudinary.uploader
import os
import datetime


class EventRoutes:
    def __init__(self):
        self.blueprint = Blueprint('event_routes', __name__)
        self.model = EventModel()
        self.schema = EventSchema()
        self._register_routes()

    def _register_routes(self):
        self.blueprint.add_url_rule('/events', view_func=self.get_all_events_route, methods=['GET'])
        self.blueprint.add_url_rule('/events/<int:event_id>', view_func=self.get_event_route, methods=['GET'])
        self.blueprint.add_url_rule('/events', view_func=self.create_event_route, methods=['POST'])
        self.blueprint.add_url_rule('/events/<int:event_id>', view_func=self.update_event_route, methods=['PUT'])
        self.blueprint.add_url_rule('/events/<int:event_id>', view_func=self.delete_event_route, methods=['DELETE'])


    def get_all_events_route(self):
        """
        Obtiene todos los eventos registrados.
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
        Crea un nuevo evento con validación y subida de imagen.
        """
        try:
            data = request.form.to_dict()
            validated_data = self.schema.load(data)

            # Manejar subida de imagen si existe
            if 'image' in request.files:
                image_file = request.files['image']
                print("Imagen recibida:", image_file.filename)  # Agrega esta línea para depuración
                validated_data['image_name'] = self._upload_image_to_cloudinary(image_file)
            else:
                validated_data['image_name'] = None


            # Establecer fecha de creación adicional si es necesario
            validated_data['create_date'] = datetime.datetime.utcnow()

            # Crear evento en la base de datos
            new_event_id = self.model.create_event(validated_data)
            return jsonify({"message": "Evento creado", "event_id": new_event_id}), 201

        except ValidationError as ve:
            return jsonify({"error": "Datos inválidos", "details": ve.messages}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    def _upload_image_to_cloudinary(self, image_file):
        """
        Sube una imagen a Cloudinary y devuelve el nombre o identificador único.
        """
        try:
            response = cloudinary.uploader.upload(
                image_file,
                folder=os.getenv("CLOUDINARY_UPLOAD_FOLDER", "reviews")
            )
            return response.get("public_id")  # Guardar solo el identificador
        except Exception as e:
            raise Exception(f"Error al subir la imagen: {e}")


    def update_event_route(self, event_id):
        """
        Actualiza un evento existente.
        """
        try:
            data = request.form.to_dict()
            validated_data = self.schema.load(data, partial=True)

            # Manejar subida de imagen si existe
            if 'image' in request.files:
                image_file = request.files['image']
                validated_data['image_name'] = self._upload_image_to_cloudinary(image_file)

            self.model.update_event(event_id, validated_data)
            return jsonify({"message": "Evento actualizado"}), 200
        except ValidationError as ve:
            return jsonify({"error": "Datos inválidos", "details": ve.messages}), 400
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
