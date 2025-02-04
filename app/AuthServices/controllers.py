from flask_jwt_extended import get_jwt
from marshmallow import ValidationError
from .models import db, User
from .schemas import UserSchema, LoginSchema
from .utils.token import generate_access_token, generate_refresh_token
from http import HTTPStatus


BLACKLIST = set()

def register_user(data):
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


def login_user(data):
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





def logout():
    try:
        jti = get_jwt()["jti"]

        BLACKLIST.add(jti)

        return {"message": "User logged out successfully."}, HTTPStatus.OK
    except Exception:
        return {"message": "An error occurred while logging out."}, HTTPStatus.INTERNAL_SERVER_ERROR