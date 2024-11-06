from  .users import users_bp
def register_bp(app):
    app.register_blueprint(users_bp, url_prefix='/api')
