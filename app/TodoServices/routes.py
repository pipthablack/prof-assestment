from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Resource
from flask import request  


from .dto import  todo_ns, todo_model, create_todo_model, update_todo_model




from .controller import create_todo, get_todos, get_todo, update_todo




@todo_ns.route('/create', methods=["POST"])
class TodoList(Resource):
    @todo_ns.expect(create_todo_model)
    @todo_ns.response(201, "Todo created successfully.")
    @todo_ns.response(400, "Bad Request")
    @jwt_required()
    def post(self):
        """Create a new todo."""
        try:
            data = request.get_json()  # Ensure JSON payload is parsed
            current_user = get_jwt_identity()
            return create_todo(data, current_user)
        except Exception as e:
            return {"error": str(e)}, 400

    

    

@todo_ns.route("/get", methods=["GET"])
class GetTodosResource(Resource):
    @jwt_required()
    @todo_ns.marshal_with(todo_model, as_list=True)
    def get(self):
        current_user = get_jwt_identity()
        return get_todos(current_user)
    


@todo_ns.route("/<int:todo_id>", methods=["GET"])
class GetTodoResource(Resource):
    @jwt_required()
    @todo_ns.marshal_with(todo_model)
    def get(self, todo_id):
        current_user = get_jwt_identity()
        return get_todo(todo_id, current_user)
    



@todo_ns.route("/<int:todo_id>", methods=["PUT"])
class UpdateTodoResource(Resource):

    @jwt_required()
    @todo_ns.expect(update_todo_model)
    @todo_ns.marshal_with(todo_model)
    def put(self, todo_id):
        data = request.json
        current_user = get_jwt_identity()
        return update_todo(todo_id, current_user, data)
