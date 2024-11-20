from marshmallow import Schema, fields, validate, pre_load

class UserSchema(Schema):
    """Esquema de los usuarios"""
    user_id = fields.Int(required=True, dump_only=True)  # Clave primaria, solo lectura
    email = fields.Email(required=True, unique=True, validate=validate.Length(max=100))  # Obligatorio y único
    name = fields.Str(required=True, validate=validate.Length(max=50))  # Obligatorio
    password = fields.Str(required=True, load_only=True)  # Obligatorio, solo escritura
    create_date = fields.Date(required=False)  # Opcional (se pasa en el mismo Query usando el NOW())
    university_id = fields.Int(required=False)  # Opcional
    
class LoginSchema(Schema):
    """Esquema para logear un usuario."""
    email = fields.Email(required=True, error_messages={"required": "El correo electrónico es obligatorio."})
    password = fields.String(required=True, error_messages={"required": "La contraseña es obligatoria."})
    
    @pre_load
    def ensure_password_is_string(self, data, **kwargs):
        """
        Esto convierte el password a string antes de que marshmallow lo valide
        ya que debido al hash es necesario que sea un string.
        """
        if 'password' in data:
            data['password'] = str(data['password'])
        return data