from flask import  Flask, g
from sqlalchemy.orm import sessionmaker, scoped_session
from flask_migrate import Migrate
from config import Config
from .database import db

migrate = Migrate() 

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    with app.app_context():
        db.init_app(app)
        
        # Initialize Session and ScopedSession within app context
        Session = sessionmaker(autocommit=False, autoflush=False, bind=db.engine)
        global ScopedSession
        ScopedSession = scoped_session(Session)
        migrate.init_app(app, db)  

    from .routes import register_bp
    register_bp(app)

    # @app.teardown_request
    # def teardown_request(exception=None):
    #     session = g.db_session
    #     if session:
    #         try:
    #             session.commit()  
    #         except Exception as e:
    #             session.rollback()  
    #             raise e
    #         finally:
    #             session.remove()  

    return app

def init_session():
    """Lazy-loads the session if it hasn't been initialized yet."""
    if not hasattr(g, 'db_session'):
        g.db_session = ScopedSession()
