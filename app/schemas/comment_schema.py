from marshmallow import Schema, fields

class CommentSchema(Schema):
    comment_id = fields.Int(dump_only=True)  # Clave primaria, solo escritura
    review_id = fields.Int(required=True)  # ID de la reseña a la que se comenta
    comment = fields.Str(required=True)  # Contenido del comentario obligatorio
    user_id = fields.Int(required=True)  # ID del usuario que hizo el comentario
