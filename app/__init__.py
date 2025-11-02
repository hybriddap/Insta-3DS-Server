from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)

    # Import routes after app creation (to avoid circular imports)
    from .routes import main
    app.register_blueprint(main)

    return app