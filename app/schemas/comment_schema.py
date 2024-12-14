from marshmallow import Schema, fields, validates, ValidationError


class CommentSchema(Schema):
    # Campos para validación y serialización
    comment_id = fields.Int(dump_only=True)
    review_id = fields.Int(required=True, error_messages={"required": "El campo 'review_id' es obligatorio."})
    comment = fields.Str(required=True, validate=lambda x: 1 <= len(x) <= 500, error_messages={
        "required": "El campo 'comment' es obligatorio.",
        "validator_failed": "El comentario debe tener entre 1 y 500 caracteres."
    })
    user_id = fields.Int(required=True, error_messages={"required": "El campo 'user_id' es obligatorio."})
    
    @validates("review_id")
    def validate_review_id(self, value):
        if value <= 0:
            raise ValidationError("El 'review_id' debe ser un número positivo.")

    @validates("user_id")
    def validate_user_id(self, value):
        if value <= 0:
            raise ValidationError("El 'user_id' debe ser un número positivo.")


class CommentWithUserSchema(Schema):
    # Extensión para incluir el nombre del usuario
    comment_id = fields.Int(dump_only=True)
    comment = fields.Str(dump_only=True)
    user_name = fields.Str(dump_only=True)
