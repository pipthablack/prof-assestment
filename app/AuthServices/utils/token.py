from functools import wraps
from http import HTTPStatus
import jwt
from datetime import datetime, timedelta, timezone
from flask import current_app, g, request



def generate_access_token(user):
    """Generate an access token."""
    payload = {
        'sub': str(user.id),
        'iat': datetime.now(timezone.utc),
        'exp': datetime.now(timezone.utc) + timedelta(days=7)
    }
    access_token = jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')  
    print(access_token, "hgvghfhugugjjk",)
    return access_token  

def generate_refresh_token(user):
    """Generate a refresh token."""
    payload = {
        'sub': str(user.id),
        'iat': datetime.now(timezone.utc),
        'exp': datetime.now(timezone.utc) + timedelta(days=30)
    }
    refresh_token = jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')
    print(refresh_token, "jbjbjgjgjgj")
    return refresh_token

def decode_user_jwt(auth_token, is_refresh=False):
   
    secret_key = current_app.config.get("JWT_SECRET_KEY")
    if not secret_key:
        print("JWT_SECRET_KEY is not set in the configuration")
        raise ValueError("JWT_SECRET_KEY is not set in the configuration")

    try:
        payload = jwt.decode(auth_token, secret_key, algorithms=[current_app.config.get("JWT_ALGORITHM", "HS256")])
        print("Decoded JWT token successfully")
        return payload
    except jwt.ExpiredSignatureError:
        print("Token has expired")
        raise
    except jwt.InvalidTokenError as e:
        print(f"Invalid token: {str(e)}")
        raise
    except Exception as e:
        print(f"Error decoding JWT token: {str(e)}")
        raise
    
def user_jwt_required(validate_user_id: bool = False):
    """
    Decorator to protect user-specific routes with JWT authentication.
    
    Args:
        validate_user_id (bool): Whether to validate the user ID from the token with the one in the URL.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                print("Token is missing or invalid")
                return {"message": "Token is missing or invalid"}, HTTPStatus.UNAUTHORIZED

            token = auth_header.split(" ")[1]
            try:
                decoded_token = decode_user_jwt(token)
                g.decoded_token = decoded_token
                print(f"Manually decoded token: {decoded_token}")
            except Exception as e:
                print(f"Manual token decoding failed: {e}")

            try:
                # if is_token_blacklisted(token):
                #     return {"message": "Token has been blacklisted "}, HTTPStatus.UNAUTHORIZED
                if validate_user_id:
                    user_id_from_token = decoded_token.get("sub")
                    user_id_from_url = kwargs.get("user_id")
                    if str(user_id_from_token) != str(user_id_from_url):
                        print("Unauthorized: User ID does not match")
                        return {"message": "Unauthorized"}, HTTPStatus.FORBIDDEN

                print("User JWT validated successfully")
                return func(*args, **kwargs)

            except jwt.ExpiredSignatureError:
                return {"message": "Token has expired"}, HTTPStatus.UNAUTHORIZED
            except jwt.InvalidTokenError as e:
                return {"message": f"Invalid token: {str(e)}"}, HTTPStatus.UNAUTHORIZED

        return wrapper
    return decorator