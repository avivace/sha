#!/usr/bin/env python3

import time
import connexion
import six
from werkzeug.exceptions import Unauthorized
from flask_cors import CORS
from flask import request
from jose import JWTError, jwt
from flask_sqlalchemy import SQLAlchemy
from config import Config

JWT_ISSUER = 'smarthomeautomation'
JWT_SECRET = 'asdfasdfasdfasdfasdfasdfasdfasdfasdfa'
JWT_LIFETIME_SECONDS = 600
JWT_ALGORITHM = 'HS256'


def login():
    request.username
    request.password

def generate_token(username):
    timestamp = _current_timestamp()
    payload = {
        "iss": JWT_ISSUER,
        "iat": int(timestamp),
        "exp": int(timestamp + JWT_LIFETIME_SECONDS),
        "sub": str(username),
    }
    
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def decode_token(token):
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except JWTError as e:
        six.raise_from(Unauthorized, e)


def get_secret(user, token_info) -> str:
    return '''
    You are user_id {user} and the secret is 'wbevuec'.
    Decoded token claims: {token_info}.
    '''.format(user=user, token_info=token_info)


def _current_timestamp() -> int:
    return int(time.time())


db = SQLAlchemy()

def run(config_class=Config):
    connex_app = connexion.FlaskApp(__name__)
    app = connex_app.app
    app.config.from_object(config_class)
    CORS(app)
    connex_app.add_api('openapi.yaml')
    connex_app.run(port=8081)
    db.init_app(app)

    return app

import models

run()