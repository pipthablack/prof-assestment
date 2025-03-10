# # def generate_access_token(user):
# #     """Generate an access token."""
# #     payload = {
# #         'sub': str(user.id),
# #         'type': 'user',
# #         'iat': datetime.now(timezone.utc),
# #         'exp': datetime.now(timezone.utc) + timedelta(days=7),
# #         'jti': str(uuid.uuid4())
# #     }
# #     access_token = jwt.encode(payload, current_app.config['JWT_SECRET_USER'], algorithm='HS256')
# #     logger.info(f"Generated access token for user {user.id}")
# #     return access_token  

# # def generate_refresh_token(user):
# #     """Generate a refresh token."""
# #     payload = {
# #         'sub': str(user.id),
# #         'type': 'user',
# #         'iat': datetime.now(timezone.utc),
# #         'exp': datetime.now(timezone.utc) + timedelta(days=30),
# #         'jti': str(uuid.uuid4())
# #     }
# #     refresh_token = jwt.encode(payload, current_app.config['JWT_SECRET_USER'], algorithm='HS256')
# #     logger.info(f"Generated refresh token for user {user.id}")
# #     return refresh_token

# from flask_jwt_extended import get_jwt, jwt_required
# import jwt

# from app.AuthServices.models import User


# def decode_user_jwt(auth_token, is_refresh=False):
   
#     secret_key = current_app.config.get("JWT_SECRET_USER")
#     if not secret_key:
#         logger.error("JWT_SECRET_USER is not set in the configuration")
#         raise ValueError("JWT_SECRET_USER is not set in the configuration")

#     try:
#         payload = jwt.decode(auth_token, secret_key, algorithms=[current_app.config.get("JWT_ALGORITHM", "HS256")])
#         logger.info("Decoded JWT token successfully")
#         return payload
#     except jwt.ExpiredSignatureError:
#         logger.warning("Token has expired")
#         raise
#     except jwt.InvalidTokenError as e:
#         logger.warning(f"Invalid token: {str(e)}")
#         raise
#     except Exception as e:
#         logger.error(f"Error decoding JWT token: {str(e)}")
#         raise


# # def is_token_blacklisted(token):
# #     """Check if the token is blacklisted."""
# #     try:
# #         decoded_token = jwt.decode(token, current_app.config["JWT_SECRET_USER"], algorithms=["HS256"])
# #         jti = decoded_token.get("jti")
        
# #         # Check in Redis
# #         logger.info(f"Checking if token {jti} is blacklisted")
# #         if redis_client.get(jti) == "blacklisted":
# #             logger.info(f"Token {jti} is blacklisted")
# #             return True 
        
# #         return False
# #     except jwt.ExpiredSignatureError:
# #         logger.warning("Token has expired")
# #         return True  
# #     except jwt.InvalidTokenError:
# #         logger.warning("Invalid token")
# #         return True 
# from asyncio.log import logger
# from functools import wraps
# from http import HTTPStatus
# from urllib import request

# from flask import current_app, g, jsonify


# def user_jwt_required(validate_user_id: bool = False):
#     """
#     Decorator to protect user-specific routes with JWT authentication.
    
#     Args:
#         validate_user_id (bool): Whether to validate the user ID from the token with the one in the URL.
#     """
#     def decorator(func):
#         @wraps(func)
#         @jwt_required()
#         def wrapper(*args, **kwargs):
#             # auth_header = request.headers.get("Authorization")
#             try:
#                 # Get the decoded JWT data
#                 jwt_data = get_jwt()
#                 print("JWT Data:", jwt_data)  # Debugging line

#                 user_id = jwt_data.get("sub")  # Extract 'sub' field (user_id) from the JWT
#                 print("User ID from token:", user_id)  # Debugging line

#                 if not user_id:
#                     return jsonify({"message": "User ID is missing in the token"}), HTTPStatus.BAD_REQUEST

#                 # Fetch the user from the database
#                 user = User.query.get(user_id)
#                 if not user:
#                     return jsonify({"message": "User not found"}), HTTPStatus.NOT_FOUND

#                 # Attach the user object to the request context
#                 request.user = user
#                 return func(*args, **kwargs)
#             except Exception as e:
#                 return jsonify({"message": "An error occurred", "error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
#             # try:
#             #     if is_token_blacklisted(token):
#             #         return {"message": "Token has been blacklisted "}, HTTPStatus.UNAUTHORIZED
#             #     if validate_user_id:
#             #         user_id_from_token = decoded_token.get("sub")
#             #         user_id_from_url = kwargs.get("user_id")
#             #         if str(user_id_from_token) != str(user_id_from_url):
#             #             logger.warning("Unauthorized: User ID does not match")
#             #             return {"message": "Unauthorized"}, HTTPStatus.FORBIDDEN

#             #     logger.info("User JWT validated successfully")
#             #     return func(*args, **kwargs)

#             # except jwt.ExpiredSignatureError:
#             #     return {"message": "Token has expired"}, HTTPStatus.UNAUTHORIZED
#             # except jwt.InvalidTokenError as e:
#             #     return {"message": f"Invalid token: {str(e)}"}, HTTPStatus.UNAUTHORIZED

#         return wrapper
#     return decorator