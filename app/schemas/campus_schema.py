from marshmallow import Schema, fields, validate

class CampusSchema(Schema):
    campus_id = fields.Int(dump_only=True)  # Clave primaria, solo escritura
    name = fields.Str(required=True, unique=True, validate=validate.Length(max=100))  # Nombre de campus obligatorio y único
