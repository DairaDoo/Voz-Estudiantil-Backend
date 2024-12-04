from marshmallow import Schema, fields, validate

class ProfessorSchema(Schema):
    """Esquema para los profesores"""
    professor_id = fields.Int(required=True, dump_only=True)  # Clave primaria, solo lectura
    name = fields.Str(required=True, validate=validate.Length(max=100))  # Nombre del profesor
    department = fields.Str(validate=validate.Length(max=100))  # Departamento opcional
    university_id = fields.Int(required=True)  # Clave foránea hacia la universidad
    created_at = fields.DateTime(dump_only=True)  # Fecha de creación, solo lectura
    updated_at = fields.DateTime(dump_only=True)  # Fecha de actualización, solo lectura
