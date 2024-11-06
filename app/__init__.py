from flask import Flask,g
from sqlalchemy.orm import sessionmaker, scoped_session
from ..config import Config
from .database import db


Session = sessionmaker(autocommit=False, autoflush=False, bind=db.engine)
ScopedSession = scoped_session(Session)
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from .routes import register_bp
    register_bp(app)

    @app.teardown_request
    def teardown_request(exception=None):
        session = getattr(g, 'db_session', None)
        if session:
            try:
                session.commit()  
            except Exception as e:
                session.rollback()  
                raise e
            finally:
                session.remove()  
    return app

def init_session():
    if not hasattr(g, 'db_session'):
        g.db_session = ScopedSession()  #