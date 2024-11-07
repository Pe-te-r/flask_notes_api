from  .users import users_bp
from .notes import notes_bp
def register_bp(app):
    app.register_blueprint(users_bp, url_prefix='/api')
    app.register_blueprint(notes_bp, url_prefix='/api')
    