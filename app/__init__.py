from flask import Flask

def create_app():
    app = Flask(__name__)

    # Import routes after app creation (to avoid circular imports)
    from .routes import main
    app.register_blueprint(main)

    return app