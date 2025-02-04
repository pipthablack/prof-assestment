from app import db 
from werkzeug.security import generate_password_hash, check_password_hash
import re 



class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, first_name, last_name , email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        """Hashes the password and sets the password_hash."""
        if not self.validate_password(password):
            raise ValueError(
                "Password must be at least 8 characters long, start with a capital letter, and include a special character."
            )
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        """Validate password according to specific rules."""
        # Check for minimum length, capital letter at the start, and at least one special character
        pattern = r'^[A-Z](?=.*[!@#$%^&*(),.?":{}|<>]).{7,}$'
        return bool(re.match(pattern, password))

    def check_password(self, password):
        """Check if the provided password matches the stored hash."""
        return check_password_hash(self.password_hash, password)
    

