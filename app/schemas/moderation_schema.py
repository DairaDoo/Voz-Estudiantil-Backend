from marshmallow import Schema, fields, validate

class ModerationSchema(Schema):
    moderation_id = fields.Int(dump_only=True)  # Clave primaria, solo escritura
    item_id = fields.Int(required=True)  # ID del elemento que se revisa
    tipo = fields.Str(required=True, validate=validate.OneOf(["event", "review", "professor", "professor_responses"]))  # Tipo de contenido
    estado = fields.Str(required=True, validate=validate.OneOf(["pendiente", "aprobado", "rechazado"]))  # Estado de revisión
    motivo_rechazo = fields.Str()  # Motivo de rechazo opcional