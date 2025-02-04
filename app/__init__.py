from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_restx import Api
from .config import Config 
from flask_cors import CORS
# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Set the configuration for the app from the Config class
    app.config.from_object(Config)  # Use the Config class to set configuration
    print(f"DEBUG: {app.config['DEBUG']}, ENV: {app.config['FLASK_ENV']}")
    # app.config['SERVER_NAME'] = "https://e3dc-102-89-68-34.ngrok-free.app"

    # Initialize the db with the app
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app, resources={r"/*": {"origins": ["https://e3dc-102-89-68-34.ngrok-free.app"]}})



    # Initialize Flask-JWT-Extended
    JWTManager(app)  # Initialize JWTManager for token handling

    # Initialize Flask-RESTx API with Swagger support
    api = Api(app, 
          doc='/swagger/', 
          security='BearerAuth',  # Define the global security schema
          authorizations={
              'BearerAuth': {
                  'type': 'apiKey',
                  'in': 'header',
                  'name': 'Authorization',
                  'description': 'JWT Bearer token'
              }
          })

    # Register namespaces (ensure your namespaces are defined and imported correctly)
    with app.app_context():
        db.create_all()
        from .AuthServices.routes import authentication_ns
        from .TodoServices.routes import todo_ns
    
        api.add_namespace(authentication_ns, path='/auth/api/v1')
        api.add_namespace(todo_ns, path='/todos/api/v1')

    # Return the app instance
    return app
