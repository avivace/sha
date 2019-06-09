import time
import connexion
import six
from werkzeug.exceptions import Unauthorized
from flask_cors import CORS
from jose import JWTError, jwt
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate
from db import db
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()


def initConnexApp(config_class=Config):
    connex_app = connexion.FlaskApp(__name__)
    app = connex_app.app
    app.config.from_object(config_class)
    CORS(app)
    connex_app.add_api('openapi.yaml')

    db.init_app(app)
    migrate.init_app(app, db)

    return connex_app


import models