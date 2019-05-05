import jwt
import json
from time import time
from hashlib import md5
from datetime import datetime
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app

followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    cellular = db.Column(db.String(10), index=True, unique=True)
    is_admin = db.Column(db.Boolean, index=True, unique=False)
    is_active = db.Column(db.Boolean, index=True, unique=False)
    password_hash = db.Column(db.String(128))

    posts = db.relationship('Post', backref='author', lazy='dynamic')

    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    messages_sent = db.relationship('Message',
                                    foreign_keys='Message.sender_id',
                                    backref='author', lazy='dynamic')
    messages_received = db.relationship('Message',
                                        foreign_keys='Message.recipient_id',
                                        backref='recipient', lazy='dynamic')
    last_message_read_time = db.Column(db.DateTime)

    notifications = db.relationship('Notification', backref='user',
                                    lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

    def new_messages(self):
        last_read_time = self.last_message_read_time or datetime(1900, 1, 1)
        return Message.query.filter_by(recipient=self).filter(
            Message.timestamp > last_read_time).count()

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

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Message {}>'.format(self.body)

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
    topic = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(120), index=False, unique=False)
    stanze = db.relationship('Stanza', backref='in_piano', lazy='dynamic')

    def __repr__(self):
        return '<Piano {}>'.format(self.description)

class Stanza(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(64), index=True, unique=False)
    description = db.Column(db.String(120), index=False, unique=False)
    piano_id = db.Column(db.Integer, db.ForeignKey('piano.id'))
    attuatori = db.relationship('Attuatore', backref='in_stanza', lazy='dynamic')
    sensori = db.relationship('Sensore', backref='in_stanza', lazy='dynamic')

    def __repr__(self):
        return '<Stanza {}>'.format(self.description)

class Attuatore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(64), index=True, unique=False)
    description = db.Column(db.String(120), index=False, unique=False)
    type = db.Column(db.String(64), index=False, unique=False)
    pin = db.Column(db.Integer, index=False, unique=True)
    stanza_id = db.Column(db.Integer, db.ForeignKey('stanza.id'))

    def __repr__(self):
        return '<Attuatore {}>'.format(self.description)

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