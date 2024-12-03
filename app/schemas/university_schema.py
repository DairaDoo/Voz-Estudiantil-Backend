from marshmallow import Schema, fields

class UniversitySchema(Schema):
    """Esquema para las universidades"""
    university_id = fields.Int(required=True, dump_only=True)  # Clave primaria, solo lectura
    name = fields.Str(required=True, validate=fields.Length(max=100))  # Nombre de la universidad
