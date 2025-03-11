from http import HTTPStatus
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required
from marshmallow import ValidationError

from app.AuthServices.models import User
from app.AuthServices.schemas import UserSchema
# from app.AuthServices.utils.decorator import user_jwt_required
from .dto import authentication_ns 
from .dto import signup_model,login_model
from flask_restx import Resource
from flask import request
from .controllers import fetch_user, register_user,login_user,logout
from .utils.decorator import user_jwt_required




# Signup route
@authentication_ns.route("/signup", methods=["POST"])
class Signup(Resource):
    @authentication_ns.expect(signup_model)
    @authentication_ns.response(201, "User created successfully")
    @authentication_ns.response(400, "Bad request")
    def post(self):
        """Sign up a new user."""

        # Call the service function to handle the signup logic
        user_data = register_user()

        # Serialize the user object to send back the response
        return user_data




@authentication_ns.route("/login", methods=["POST"])
class Login(Resource):
    @authentication_ns.expect(login_model)
    @authentication_ns.response(201, "User  logged in successfully")
    @authentication_ns.response(400, "Bad request")
    def post(self):
        """Sign up a new user."""


        # Call the service function to handle the signup logic
        user_data = login_user()

        # Serialize the user object to send back the response
        return user_data


# FetchUser
@authentication_ns.route("/profile", methods=["GET"])
class Profile(Resource):
    @authentication_ns.response(200, "Profile fetched successfully")
    @authentication_ns.response(401, "Unauthorized")
    @authentication_ns.response(404, "User not found")
    @user_jwt_required()  # Ensure that a valid JWT is required to access this route
    # @jwt_required(validate_user_id = True)  # Ensure that a valid JWT is required to access this route
    def get(self):
        """Fetch user profile based on JWT token."""
        # current_user_id = get_jwt_identity() 
        result, status_code = fetch_user()  #

        return result, status_code

    

        

@authentication_ns.route("/logout", methods=["POST"])
class Logout(Resource):
    @authentication_ns.response(200, "User logged out successfully")
    @authentication_ns.response(400, "Bad request")
    @user_jwt_required()  # Ensure that a valid JWT is required to access this route
    def post(self):
        """Log Out an existing user."""
        # Call the service function to handle the signup logic
        user_data = logout()

        # Serialize the user object to send back the response
        return user_data
