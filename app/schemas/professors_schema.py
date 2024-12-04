from marshmallow import Schema, fields, validate

class ProfessorSchema(Schema):
    """Esquema para los profesores"""
    professor_id = fields.Int(dump_only=True)  # Clave primaria, solo lectura
    name = fields.Str(required=True, validate=validate.Length(max=50))  # Nombre del profesor
    department_id = fields.Int(required=True)  # Clave foránea al departamento
    overall_rating = fields.Float(dump_only=True)  # Solo lectura, calculado por el sistema
    state = fields.Str(validate=validate.OneOf(['pendiente', 'aprobado', 'rechazado']), dump_only=True)  # Estado, solo lectura
    department = fields.Nested('DepartmentSchema', dump_only=True)  # Relación anidada, solo para salida
