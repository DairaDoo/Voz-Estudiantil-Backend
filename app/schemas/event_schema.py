from marshmallow import Schema, fields, ValidationError
import datetime

class EventSchema(Schema):
    title = fields.Str(required=True)
    date = fields.Date(missing=lambda: datetime.date.today())
    description = fields.Str(required=True)
    user_id = fields.Int(required=True)
    university_id = fields.Int(required=True)
