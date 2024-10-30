from marshmallow import Schema, fields, validate

class ProfessorQuestionSchema(Schema):
    question_id = fields.Int(dump_only=True)  # Clave primaria, solo escritura
    question_text = fields.Str(required=True, validate=validate.Length(max=255))  # Texto de la pregunta
    is_question_active = fields.Bool(required=True)  # Estado activo/inactivo de la pregunta
