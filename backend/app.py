#!/usr/bin/env python3
import time

import connexion
import six
from werkzeug.exceptions import Unauthorized
from flask_cors import CORS
from flask import request
from jose import JWTError, jwt

JWT_ISSUER = 'smarthomeautomation'
JWT_SECRET = 'asdfasdfasdfasdfasdfasdfasdfasdfasdfa'
JWT_LIFETIME_SECONDS = 600
JWT_ALGORITHM = 'HS256'

def generate_token():
    # AUTHENTICATION LOGIC GOES HERE
    timestamp = _current_timestamp()
    payload = {
        "iss": JWT_ISSUER,
        "iat": int(timestamp),
        "exp": int(timestamp + JWT_LIFETIME_SECONDS),
        "sub": str(request.username),
    }

    return { "success": True,
             "token": jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
             }


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


if __name__ == '__main__':
    app = connexion.FlaskApp(__name__)
    CORS(app.app)
    app.add_api('openapi.yaml')
    app.run(port=8081)
