from marshmallow import ValidationError
from .dto import authentication_ns 
from .dto import signup_model,login_model
from flask_restx import Resource
from flask import request
from .controllers import register_user,login_user,logout




# Signup route
@authentication_ns.route("/signup", methods=["POST"])
class Signup(Resource):
    @authentication_ns.expect(signup_model)
    @authentication_ns.response(201, "User created successfully")
    @authentication_ns.response(400, "Bad request")
    def post(self):
        """Sign up a new user."""
        data = request.json

        try:

            # Call the service function to handle the signup logic
            user_data = register_user(data)

            # Serialize the user object to send back the response
            return user_data, 201

        except ValidationError as err:
            return {"message": "Validation failed", "errors": err.messages}, 400
        except ValueError as err:
            return {"message": str(err)}, 400
        except Exception as err:
            return {"message": "An unexpected error occurred", "error": str(err)}, 500



@authentication_ns.route("/login", methods=["POST"])
class Login(Resource):
    @authentication_ns.expect(login_model)
    @authentication_ns.response(201, "User  logged in successfully")
    @authentication_ns.response(400, "Bad request")
    def post(self):
        """Sign up a new user."""
        data = request.json

        try:

            # Call the service function to handle the signup logic
            user_data = login_user(data)

            # Serialize the user object to send back the response
            return user_data, 200

        except ValidationError as err:
            return {"message": "Validation failed", "errors": err.messages}, 400
        except ValueError as err:
            return {"message": str(err)}, 400
        except Exception as err:
            return {"message": "An unexpected error occurred", "error": str(err)}, 500
        

@authentication_ns.route("/logout", methods=["POST"])
class Logout(Resource):
    @authentication_ns.response(200, "User logged out successfully")
    @authentication_ns.response(400, "Bad request")
    def post(self):
        """Sign up a new user."""
        try:

            # Call the service function to handle the signup logic
            user_data = logout()

            # Serialize the user object to send back the response
            return user_data, 200

        except ValidationError as err:
            return {"message": "Validation failed", "errors": err.messages}, 400
        except ValueError as err:
            return {"message": str(err)}, 400
        except Exception as err:
            return {"message": "An unexpected error occurred", "error": str(err)}, 500