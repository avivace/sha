# coding=utf-8
from app import app, db
from app.models import User, Post, Notification, Message

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Message': Message,
            'Notification': Notification}

app.run( host = '0.0.0.0' , debug = False )
