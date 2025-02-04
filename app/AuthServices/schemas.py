from marshmallow  import Schema,fields



class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    email = fields.Email(required=True, unique=True)
    password = fields.String(load_only=True, required=True)
   



class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)