from marshmallow import Schema, fields, validate

class DepartmentSchema(Schema):
    department_id = fields.Int(dump_only=True)  # Clave primaria, solo escritura
    name = fields.Str(required=True, validate=validate.Length(max=100))  # Nombre del departamento obligatorio
    university_id = fields.Int(required=True)  # ID de la universidad asociada
