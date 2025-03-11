import jwt
from asyncio.log import logger
from functools import wraps
from http import HTTPStatus

from flask import current_app, g, request


def decode_user_jwt(auth_token, is_refresh=False):
   
    secret_key = current_app.config.get("JWT_SECRET_USER")
    if not secret_key:
        logger.error("JWT_SECRET_USER is not set in the configuration")
        raise ValueError("JWT_SECRET_USER is not set in the configuration")

    try:
        payload = jwt.decode(auth_token, secret_key, algorithms=[current_app.config.get("JWT_ALGORITHM", "HS256")])
        logger.info("Decoded JWT token successfully")
        return payload
    except jwt.ExpiredSignatureError:
        logger.warning("Token has expired")
        raise
    except jwt.InvalidTokenError as e:
        logger.warning(f"Invalid token: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Error decoding JWT token: {str(e)}")
        raise

def user_jwt_required():
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
                logger.warning("Token is missing or invalid")
                return {"message": "Token is missing or invalid"}, HTTPStatus.UNAUTHORIZED

            token = auth_header.split(" ")[1]
            decoded_token = None
            try:
                decoded_token = decode_user_jwt(token)
                g.decoded_token = decoded_token
                g.user_id = decoded_token.get("sub")
                logger.info(f"Manually decoded token: {decoded_token}")
                logger.info(f"User ID set in g object: {g.user_id}")
            except Exception as e:
                logger.error(f"Manual token decoding failed: {e}")
                return {"message": "Token is missing or invalid"}, HTTPStatus.UNAUTHORIZED

            try:
                

                logger.info("User JWT validated successfully")
                return func(*args, **kwargs)
            except jwt.ExpiredSignatureError:
                return {"message": "Token has expired"}, HTTPStatus.UNAUTHORIZED
            except jwt.InvalidTokenError as e:
                return {"message": f"Invalid token: {str(e)}"}, HTTPStatus.UNAUTHORIZED

        return wrapper
    return decorator