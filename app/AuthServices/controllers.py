from flask import request
from flask_jwt_extended import get_jwt
from marshmallow import ValidationError
from .models import db, User
from .schemas import UserSchema, LoginSchema
from .utils.token import generate_access_token, generate_refresh_token
from http import HTTPStatus


BLACKLIST = set()

def register_user():
    data = request.get_json()
    user_schema = UserSchema()

    try:
        validated_data = user_schema.load(data)
    except ValidationError as e:
        return {"error": str(e)}, HTTPStatus.BAD_REQUEST

    existing_user_by_email = User.query.filter_by(email=validated_data['email']).first()
    if existing_user_by_email:
        return {"error": "Email already exists."}, HTTPStatus.BAD_REQUEST

    new_user = User(
        first_name=validated_data['first_name'],
        last_name=validated_data['last_name'],
        email=validated_data['email'],
        password=validated_data['password']
    )
    try:
        db.session.add(new_user)
        db.session.commit()
        return {
            "user_id": new_user.id,
            "first_name": new_user.first_name,
            "last_name": new_user.last_name,
            "email": new_user.email,
            "message": "User registered successfully.",
        }, HTTPStatus.CREATED
    except Exception as e:
        db.session.rollback()
        return {"error": "An error occurred while registering the user."}, HTTPStatus.INTERNAL_SERVER_ERROR


def login_user():
    data = request.get_json()
    login_schema = LoginSchema()
    try:
        validated_data = login_schema.load(data)

        user = User.query.filter_by(email=validated_data["email"]).first()
        if not user or not user.check_password(validated_data["password"]):
            return {"error": "Invalid email or password."}, HTTPStatus.UNAUTHORIZED

        access_token = generate_access_token(user)
        refresh_token = generate_refresh_token(user)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user_id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
        }, HTTPStatus.OK
    except ValidationError as e:
        return {"error": str(e)}, HTTPStatus.BAD_REQUEST
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return {"error": "An unexpected error occurred while logging in."}, HTTPStatus.INTERNAL_SERVER_ERROR

def fetch_user(user_id):
    try:
        # Get the current JWT token data (we expect 'sub' to be the user ID)
        # jwt_data = get_jwt()
        # user_id = jwt_data["sub"]  # "sub" is the standard claim for user ID in JWTs

        # Fetch the user from the database using the extracted user ID
        user = User.query.get(user_id)

        # Check if the user exists
        if not user:
            return {"error": "User not found."}, HTTPStatus.NOT_FOUND

        # Return user details (you can customize the response to include any fields you need)
        return {
            "user_id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "message": "User data retrieved successfully."
        }, HTTPStatus.OK
    except Exception as e:
        print(f"Exception occurred in fetch_user: {str(e)}")
        return {"error": "An error occurred while fetching user data."}, HTTPStatus.INTERNAL_SERVER_ERROR


def logout():
    try:
        jti = get_jwt()["jti"]

        BLACKLIST.add(jti)

        return {"message": "User logged out successfully."}, HTTPStatus.OK
    except Exception:
        return {"message": "An error occurred while logging out."}, HTTPStatus.INTERNAL_SERVER_ERROR