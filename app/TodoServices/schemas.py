from marshmallow import Schema, fields




class TodoSchema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String(required=True)
    description = fields.String(required=True)
    # user_id = fields.Integer(required=True) 
    created_at = fields.DateTime(dump_only=True)


class UpdateTodoSchema(Schema):
    title = fields.String()
    description = fields.String()
    user_id = fields.Integer()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    is_completed = fields.Boolean(dump_only=True)