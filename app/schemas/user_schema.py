from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    user_id = fields.Int(required=True, dump_only=True)  # Clave primaria, solo lectura
    email = fields.Email(required=True, unique=True, validate=validate.Length(max=100))  # Obligatorio y único
    name = fields.Str(required=True, validate=validate.Length(max=50))  # Obligatorio
    password = fields.Str(required=True, load_only=True)  # Obligatorio, solo escritura
    create_date = fields.Date(required=True)  # Obligatorio
