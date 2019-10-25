from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    # Init flask app
    app = Flask(__name__, instance_relative_config=False)

    # Flask app config
    app.config.from_object('config.Config')

    # Initialize Plugins
    db.init_app(app)
    login_manager.login_view = 'auth_bp.login'
    login_manager.init_app(app)
    
    with app.app_context():
        from . import routes
        from . import auth

        app.register_blueprint(routes.main_bp)
        app.register_blueprint(auth.auth_bp)

        # create database models
        db.create_all()

        return app
