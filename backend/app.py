import time
import connexion
import six
from werkzeug.exceptions import Unauthorized
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()


def initConnexApp(config_class=Config):
    # Create Connexion App
    connex_app = connexion.FlaskApp(__name__)
    # Expose the wrapped FlaskApp object
    app = connex_app.app
    # Apply our configuration
    app.config.from_object(config_class)
    # Enable CORS for everything
    CORS(app)
    # Add our defined API
    connex_app.add_api('openapi.yaml')
    # Get the DB up and running
    db.init_app(app)

    return connex_app


import models