from flask_restx import fields, Namespace


# Create the Namespace for authentication
authentication_ns = Namespace("auth", description="User operations")

# Signup model
signup_model = authentication_ns.model(
    "UserSignup",
    {
        "first_name": fields.String(
            required=True, description="First Name", min_length=3
        ),
         "last_name": fields.String(
            required=True, description="Last Name", min_length=3
        ),
        "email": fields.String(required=True, description="Email"),
        "password": fields.String(
            required=True, description="Password", min_length=8
        ),
    }
)

# Login model
login_model = authentication_ns.model(
    "Login",
    {
        "email": fields.String(required=True, description="Email"),
        "password": fields.String(required=True, description="Password"),
    }
)