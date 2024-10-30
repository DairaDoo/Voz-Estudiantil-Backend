from marshmallow import Schema, fields

class ProfessorResponseSchema(Schema):
    response_id = fields.Int(dump_only=True)  # Clave primaria, solo escritura
    user_id = fields.Int(required=True)  # ID del usuario que respondió
    professor_id = fields.Int(required=True)  # ID del profesor evaluado
    question_id = fields.Int(required=True)  # ID de la pregunta respondida
    answer = fields.Int(required=True, validate= lambda x: 1 <= x <= 5)  # Calificación (1 a 5)
    