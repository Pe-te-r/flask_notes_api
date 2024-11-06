from flask import Flask
from ..config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from .routes import register_bp
    register_bp(app)
    return app