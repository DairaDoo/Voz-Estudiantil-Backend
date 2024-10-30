from marshmallow import Schema, fields, validate

class UniversitySchema(Schema):
    university_id = fields.Int(dump_only=True)  # Clave primaria, solo escritura
    name = fields.Str(required=True, unique=True, validate=validate.Length(max=100))  # Nombre de la universidad obligatorio y único
    campus_id = fields.Int(required=True)  # ID del campus asociado