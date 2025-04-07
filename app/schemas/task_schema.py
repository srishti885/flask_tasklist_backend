from marshmallow import Schema, fields, validate

class TaskSchema(Schema):
    id = fields.Int(dump_only=True)
    task_name = fields.Str(required=True, validate=validate.Length(min=1))
    is_active = fields.Bool(load_default=True)
