from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import metadata
from flaskdb import db

from templates.apps.views import app_blueprint

def create_app():
    app = Flask(__name__,
        static_folder = './public',
        template_folder="./static")

    app.config.from_object('configurations.DevelopmentConfig')

    db.init_app(app)

    with app.app_context():
        db.create_all()

    # register the blueprints
    app.register_blueprint(app_blueprint)

    return app
