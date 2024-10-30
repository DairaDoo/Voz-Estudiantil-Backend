from marshmallow import Schema, fields, validate

class ReportCategorySchema(Schema):
    report_category_id = fields.Int(dump_only=True)  # Clave primaria, solo escritura 
    category_name = fields.Str(required=True, unique=True, validate=validate.Length(max=50))  # Nombre de la categoría obligatorio y único
