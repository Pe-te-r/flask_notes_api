from flask import  Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from config import Config
from .database import db

migrate = Migrate() 

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    with app.app_context():
        db.init_app(app)

        JWTManager(app)   

        migrate.init_app(app, db)  

    from .routes import register_bp
    register_bp(app)


    return app
