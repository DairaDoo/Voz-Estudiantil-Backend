from marshmallow import Schema, fields, validate

class ProfessorSchema(Schema):
    profesor_id = fields.Int(dump_only=True)  # Clave primaria, solo escritura
    name = fields.Str(required=True, validate=validate.Length(max=100))  # Nombre obligatorio
    department_id = fields.Int(required=True)  # ID del departamento
    overall_rating = fields.Float()  # Promedio de rating
    state = fields.Str(validate=validate.OneOf(["pendiente", "aprobado", "rechazado"]))  # Estado de revisión
