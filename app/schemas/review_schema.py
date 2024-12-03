from marshmallow import Schema, fields, validates, ValidationError
from datetime import datetime

class ReviewSchema(Schema):
    review_id = fields.Int(dump_only=True)  # Solo se devuelve en respuestas, no se acepta en solicitudes
    review = fields.Str(
        required=True,
        validate=lambda x: len(x.strip()) > 0,
        error_messages={"required": "La reseña es obligatoria.", "validator_failed": "La reseña no puede estar vacía."}
    )
    user_id = fields.Int(required=True, error_messages={"required": "El ID del usuario es obligatorio."})
    image_name = fields.Str(allow_none=True)
    create_date = fields.DateTime(
        dump_only=True,  # Solo se genera automáticamente, no se espera en solicitudes
        default=datetime.utcnow
    )
    up_vote = fields.Int(missing=0, error_messages={"invalid": "El número de votos positivos debe ser un entero."})
    down_vote = fields.Int(missing=0, error_messages={"invalid": "El número de votos negativos debe ser un entero."})
    university_id = fields.Int(required=True, error_messages={"required": "El ID de la universidad es obligatorio."})
    state = fields.Str(
        required=True,
        error_messages={"required": "El estado es obligatorio."}
    )
    campus_id = fields.Int(allow_none=True)  # Este campo es opcional (puede ser nulo)

    @validates("state")
    def validate_state(self, value):
        """
        Valida que el estado sea uno de los valores permitidos.
        """
        allowed_states = ["pendiente", "aprobado", "rechazado"]
        if value.lower() not in allowed_states:
            raise ValidationError(f"Estado no válido. Debe ser uno de: {', '.join(allowed_states)}.")
    
    @validates("review")
    def validate_review_content(self, value):
        """
        Valida que la reseña no esté vacía después de eliminar espacios en blanco.
        """
        if not value.strip():
            raise ValidationError("La reseña no puede estar vacía.")

