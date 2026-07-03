from flask import Flask
from extensions.jwt import jwt
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

# Initialize extensions without an app instance.
# These global objects are imported by other files (like routes/auth_routes.py)
# so they must be defined at the top level, but NOT initialized with the app.
db = SQLAlchemy()
csrf = CSRFProtect()


def create_app():
    """
    The Application Factory Function.
    Creates and configures the Flask application instance.
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    # 1. Initialize extensions with the application instance
    db.init_app(app)
    jwt.init_app(app)
    csrf.init_app(app)  # Adding CSRF protection for forms

    # 2. Register routes/blueprints
    # The blueprint import MUST happen *inside* the factory function
    # to avoid the circular dependency issue.
    # When create_app() is called, this import happens after 'db' is defined globally.
    from routes.auth_routes import auth_bp
    from routes.user_routes import user_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)

    # 3. Create database tables within the application context
    with app.app_context():
        # Ensure all models are imported so SQLAlchemy knows about them
        # E.g., from models.user import User # (If not already imported by routes)
        db.create_all()

    return app


# IMPORTANT: Remove 'app = create_app()' from the global scope.
# The app is only created when explicitly run below, or by a WSGI server.

if __name__ == '__main__':
    # Create the app instance only when the file is executed directly
    app = create_app()
    app.run(debug=True)