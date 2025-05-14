# app.py (Modified)

from flask import Flask
from flask_login import LoginManager

# Absolute imports should now work because the project root
# will be treated correctly as a package base when running
# via the factory or 'flask run'.
from models.base import db
from blueprints import all_blueprints

# Initialize extensions outside the factory, but link inside
login_manager = LoginManager()

def create_app():
    """Application factory function."""
    app = Flask(__name__)

    # configure the SQLite database
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"

    # initialize the app with the extensions
    db.init_app(app) # Initialize db with the app instance
    login_manager.init_app(app) # Initialize login_manager with the app instance

    # Register blueprints
    for bp in all_blueprints:
        app.register_blueprint(bp)

    # Define root route (or move this to a blueprint)
    @app.route('/')
    def root():
        """Root of our app"""
        return "Hello world!"

    # Return the configured app instance
    return app

# This block is mainly for running the app directly for development
# Production servers like Gunicorn/Waitress will call create_app()
if __name__ == '__main__':
    app = create_app() # Create app instance
    with app.app_context():
        db.create_all() # Create tables within app context
    app.run(debug=True)
