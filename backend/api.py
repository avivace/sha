from flask import request
from models import User
import time
from jose import JWTError, jwt
from app import db

JWT_ISSUER = 'smarthomeautomation'
JWT_SECRET = 'asdfasdfasdfasdfasdfasdfasdfasdfasdfa'
JWT_LIFETIME_SECONDS = 600
JWT_ALGORITHM = 'HS256'


def login():
    data = request.get_json()
    user = User.query.filter_by(
        username=data["username"], is_active=True).first()

    if user is None or not user.check_password(data["password"]):
        return 400
    else:
        return {"success": True, "token": generate_token(data["username"])}


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
    '''.format(
        user=user, token_info=token_info)


def _current_timestamp() -> int:
    return int(time.time())