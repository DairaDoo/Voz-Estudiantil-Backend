from marshmallow import Schema, fields, validates, ValidationError

class DepartmentSchema(Schema):
    department_id = fields.Int(dump_only=True)  # Solo se devuelve en respuestas, no se acepta en solicitudes
    name = fields.Str(
        required=True,
        validate=lambda x: len(x.strip()) > 0,
        error_messages={
            "required": "El nombre del departamento es obligatorio.",
            "validator_failed": "El nombre del departamento no puede estar vacío."
        }
    )
    university_id = fields.Int(
        required=True,
        error_messages={"required": "El ID de la universidad es obligatorio."}
    )

    @validates("name")
    def validate_name(self, value):
        """
        Valida que el nombre del departamento no esté vacío y tenga un formato válido.
        """
        if not value.strip():
            raise ValidationError("El nombre del departamento no puede estar vacío.")
        if len(value) > 50:
            raise ValidationError("El nombre del departamento no puede tener más de 50 caracteres.")
