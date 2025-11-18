import os
from datetime import timedelta
from flask import Flask
from flask_cors import CORS
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from .config import Config
from .db import db, migrate
from .routes.health import blp as health_blp
from .routes.auth import blp as auth_blp
from .routes.users import blp as users_blp
from .routes.events import blp as events_blp
from .routes.schedules import blp as schedules_blp
from .routes.registrations import blp as registrations_blp
from .routes.notifications import blp as notifications_blp


jwt = JWTManager()


def _register_error_handlers(app: Flask) -> None:
    """Register generic error handlers and JWT callbacks."""
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return {"message": "Token has expired"}, 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error_string):
        return {"message": "Invalid token"}, 401

    @jwt.unauthorized_loader
    def missing_token_callback(error_string):
        return {"message": "Authorization token required"}, 401


# PUBLIC_INTERFACE
def create_app() -> Flask:
    """Create and configure the Flask application.

    Returns:
        Flask: Configured Flask app with DB, JWT, CORS, and registered blueprints.
    """
    app = Flask(__name__)

    # App config and OpenAPI docs
    app.config.from_object(Config)
    app.url_map.strict_slashes = False

    # CORS: allow frontend on 3000
    CORS(
        app,
        resources={r"/api/*": {"origins": app.config.get("CORS_ORIGINS", ["http://localhost:3000"])}},
        supports_credentials=True,
    )

    # OpenAPI/Swagger config
    app.config["API_TITLE"] = "Event Management API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/docs"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = ""
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    # Extensions
    api = Api(app)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    _register_error_handlers(app)

    # Blueprints
    api.register_blueprint(health_blp)
    api.register_blueprint(auth_blp)
    api.register_blueprint(users_blp)
    api.register_blueprint(events_blp)
    api.register_blueprint(schedules_blp)
    api.register_blueprint(registrations_blp)
    api.register_blueprint(notifications_blp)

    @app.get("/")
    def root():
        """Health root."""
        return {"message": "Healthy"}

    return app
