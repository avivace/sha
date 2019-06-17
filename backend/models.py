import jwt
import json
from time import time
from hashlib import md5
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from hashlib import sha512

def hash_password(password):
    salt = "1234780asa231"
    fullstring = password + salt;
    return sha512(fullstring.encode('utf-8')).hexdigest()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    cellular = db.Column(db.String(10), index=True, unique=True)
    is_admin = db.Column(db.Boolean, index=True, unique=False)
    is_active = db.Column(db.Boolean, index=True, unique=False)
    password_hash = db.Column(db.String(128))

    about_me = db.Column(db.String(140))

    notifications = db.relationship('Notification', backref='user',
                                    lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = hash_password(password)
        #generate_password_hash(password=password,method='pbkdf2:sha1',)

    def check_password(self, password):
        return self.password_hash == password

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def new_requests(self):
        return User.query.filter_by(is_active=False).count()

    def add_notification(self, name, data):
        self.notifications.filter_by(name=name).delete()
        n = Notification(name=name, payload_json=json.dumps(data), user=self)
        db.session.add(n)
        return n

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.Float, index=True, default=time)
    payload_json = db.Column(db.Text)

    def get_data(self):
        return json.loads(str(self.payload_json))

class Piano(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #topic = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(120), index=False, unique=False)
    stanze = db.relationship('Stanza', backref='in_piano', lazy='dynamic')

    def __repr__(self):
        return '<Piano {}>'.format(self.description)

class Stanza(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #topic = db.Column(db.String(64), index=True, unique=False)
    description = db.Column(db.String(120), index=False, unique=False)
    piano_id = db.Column(db.Integer, db.ForeignKey('piano.id'))
    attuatori = db.relationship('Attuatore', backref='in_stanza', lazy='dynamic')
    sensori = db.relationship('Sensore', backref='in_stanza', lazy='dynamic')

    def __repr__(self):
        return '<Stanza {}>'.format(self.description)

class Attuatore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #topic = db.Column(db.String(64), index=True, unique=False)
    description = db.Column(db.String(120), index=False, unique=False)
    type = db.Column(db.String(64), index=False, unique=False)
    pin = db.Column(db.Integer, index=False, unique=True)
    status = db.Column(db.Boolean, index=True, unique=False)

    stanza_id = db.Column(db.Integer, db.ForeignKey('stanza.id'))
    def toggle(self):
        self.status = not self.status
    def __repr__(self):
        return '<Attuatore {}>'.format(self.description)
    def update(self, description, type, pin, stanza):
        self.description = description
        self.type = type
        self.pin = pin
        self.stanza_id = stanza


class Pulsante(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    attuatore_id = db.Column(db.String(64), index=True, unique=False)
    description = db.Column(db.String(120), index=False, unique=False)
    pin = db.Column(db.Integer, index=False, unique=True)
    stanza_id = db.Column(db.Integer, db.ForeignKey('stanza.id'))

    def __repr__(self):
        return '<Pulsante {}>'.format(self.description)

class Sensore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(64), index=True, unique=False)
    description = db.Column(db.String(120), index=False, unique=False)
    type = db.Column(db.String(64), index=False, unique=False)
    pin = db.Column(db.Integer, index=False, unique=True)
    stanza_id = db.Column(db.Integer, db.ForeignKey('stanza.id'))
    letture = db.relationship('Lettura', backref='a_sensore', lazy='dynamic')

    def __repr__(self):
        return '<Sensore {}>'.format(self.description)

class Lettura(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    temperatura = db.Column(db.Float, index=False, unique=False)
    umidita = db.Column(db.Float, index=False, unique=False)
    sensore_id = db.Column(db.Integer, db.ForeignKey('sensore.id'))

    def __repr__(self):
        return '<Lettura avvenuta in data {}, pari a {}>'.format(self.timestamp, self.value)

class Riscaldamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    set_temperatura = db.Column(db.Float, index=False, unique=False)
    start_temperatura = db.Column(db.Float, index=False, unique=False, nullable=True)
    set_orario = db.Column(db.DateTime, index=False, unique=False)
    start_orario = db.Column(db.DateTime, index=True, unique=False)
    stop_orario = db.Column(db.DateTime, index=True, unique=False, nullable=True)
    attuatore_id = db.Column(db.Integer, db.ForeignKey('attuatore.id'))