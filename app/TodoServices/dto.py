from flask_restx import fields, Namespace


todo_ns = Namespace('todos', description='Todo operations')



# Todo model    
todo_model = todo_ns.model('Todo', {
    'id': fields.Integer(readonly=True, description='The unique identifier'),
    'title': fields.String(required=True, description='The title of the todo'),
    'description': fields.String(required=True, description='The description of the todo'),
    'created_at': fields.DateTime(readonly=True, description='Date when the todo was created'),
    'user_id': fields.Integer(required=True, description='The user who created the todo')
})


# Update Todo model


update_todo_model = todo_ns.model('UpdateTodo', {
    'title': fields.String(description='The title of the todo'),
    'description': fields.String(description='The description of the todo')
})



# Create Todo model

create_todo_model = todo_ns.model('CreateTodo', {
    'title': fields.String(required=True, description='The title of the todo'),
    'description': fields.String(required=True, description='The description of the todo'),
    
})


