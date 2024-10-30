from marshmallow import Schema, fields, validate

class ReportSchema(Schema):
    report_id = fields.Int(dump_only=True)  # Clave primaria, solo escritura
    user_id = fields.Int(required=True)  # ID del usuario que reportó
    report_category_id = fields.Int(required=True)  # ID de la categoría del reporte
    description = fields.Str(validate=validate.Length(max=255))  # Descripción del reporte opcional
    review_id = fields.Int(required=True)  # ID de la reseña que se reporta
