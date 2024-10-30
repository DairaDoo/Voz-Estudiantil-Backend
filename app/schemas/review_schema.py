from marshmallow import Schema, fields, validate

class ReviewSchema(Schema):
    review_id = fields.Int(required=True, dump_only=True)  # Clave primaria, solo lectura
    review = fields.Str(required=True)  # Contenido obligatorio
    title = fields.Str(required=True) # Titulo obligatorio
    user_id = fields.Int(required=True)  # ID del usuario obligatorio
    create_date = fields.Date(required=True)  # Fecha obligatoria
    image_name = fields.Str(validate=validate.Length(max=100))  # Nombre de imagen opcional