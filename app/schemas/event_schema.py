from marshmallow import Schema, fields, validate

class EventSchema(Schema):
    event_id = fields.Int(dump_only=True)  # Clave primaria
    event_title = fields.Str(required=True, validate=validate.Length(max=100))  # Título obligatorio
    description = fields.Str(required=True)  # Descripción obligatoria
    image_name = fields.Str(validate=validate.Length(max=100))  # Nombre de imagen opcional
    date = fields.Date(required=True)  # Fecha obligatoria
    user_id = fields.Int(required=True)  # ID del usuario que creó el evento
