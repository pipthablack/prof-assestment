import jwt
from datetime import datetime, timedelta, timezone
from flask import current_app



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

