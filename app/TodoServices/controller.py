from flask_jwt_extended import get_jwt_identity
from marshmallow import ValidationError
from .models import db, Todo
from .schemas import TodoSchema,UpdateTodoSchema

from http import HTTPStatus


def create_todo(data, current_user):
    todo_schema = TodoSchema()

    try:
        validated_data = todo_schema.load(data)
        new_todo = Todo(
            title=validated_data['title'],
            description=validated_data['description'],
            user_id=current_user,
        )
        db.session.add(new_todo)
        db.session.commit()
        return {
            "message": "Todo created successfully.",
            "data": todo_schema.dump(new_todo)
        }, HTTPStatus.CREATED
    except ValidationError as e:
        return {"error": str(e)}, HTTPStatus.BAD_REQUEST
    except Exception as e:
        return {
            "message": "An unexpected error occurred",
            "error": str(e)
        }, HTTPStatus.INTERNAL_SERVER_ERROR



def get_todos(user_id):
    todos = Todo.query.filter_by(user_id=user_id).all()
    todo_schema = TodoSchema(many=True)
    todos_data = todo_schema.dump(todos)
    return {"data": todos_data}, HTTPStatus.OK


def get_todo(todo_id, user_id):
    todo = Todo.query.filter_by(id=todo_id, user_id=user_id).first_or_404()
    todo_schema = TodoSchema()
    todo_data = todo_schema.dump(todo)
    return {"data": todo_data}, HTTPStatus.OK


def update_todo(todo_id, user_id, data):
    todo = Todo.query.filter_by(id=todo_id, user_id=user_id).first_or_404()
    todo_schema = UpdateTodoSchema()

    try:
        validated_data = todo_schema.load(data)
        todo.title = validated_data.get('title', todo.title)
        todo.description = validated_data.get('description', todo.description)
        todo.updated_at = db.func.now()
        db.session.commit()
        return {"message": "Todo updated successfully."}, HTTPStatus.OK
    except ValidationError as e:
        return {"error": str(e)}, HTTPStatus.BAD_REQUEST
    except Exception as e:
        return {"message": "An unexpected error occurred", "error": str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR
