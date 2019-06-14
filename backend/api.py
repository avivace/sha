from flask import request
from models import User, Post, Piano, Stanza, Attuatore, Sensore, Message, Notification, Pulsante, Riscaldamento
import time
from jose import JWTError, jwt
from app import db
import paho.mqtt.client as mqttc

JWT_ISSUER = 'smarthomeautomation'
JWT_SECRET = 'asdfasdfasdfasdfasdfasdfasdfasdfasdfa'
JWT_LIFETIME_SECONDS = 600
JWT_ALGORITHM = 'HS256'

client = mqttc.Client()
client.connect("127.0.0.1", 1883, 60)

# Utilities
def _current_timestamp() -> int:
    return int(time.time())

# Auth

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

# Main routes entry points

def login():

    data = request.get_json()
    user = User.query.filter_by(
        username=data["username"], is_active=True).first()

    if user is None or not user.check_password(data["password"]):
        return "Authentication error", 401
    else:
        return {"success": True, "token": generate_token(data["username"])}


def get_secret(user, token_info) -> str:
    return '''
    You are user_id {user} and the secret is 'wbevuec'.
    Decoded token claims: {token_info}.
    '''.format(
        user=user, token_info=token_info)

def add_device():
    data = request.get_json()
    print(data)
    device = Attuatore(topic=data["topic"],
                       description=data["description"],
                       type=data["type"],
                       pin=data["pin"],
                       stanza_id=1)
    db.session.add(device)
    db.session.commit()
    return "OK"

def overview():
    piani = Piano.query.all()

    pianiArray = []
    stanzeArray = []
    attuatoriArray = []

    for piano in piani:
        pianoObj = {}
        pianoObj['id'] = piano.id
        pianoObj['description'] = piano.description
        stanze = Stanza.query.filter_by(piano_id=piano.id).all()
        for stanza in stanze:
            stanzaObj = {}
            stanzaObj['id'] = stanza.id
            stanzaObj['description'] = stanza.description
            attuatori = Attuatore.query.filter_by(stanza_id=stanza.id)
            for attuatore in attuatori:
                attuatoreObj = {}
                attuatoreObj['id'] = attuatore.id
                attuatoreObj['pin'] = attuatore.pin
                attuatoreObj['type'] = attuatore.type
                attuatoreObj['status'] = int(attuatore.status)
                attuatoreObj['topic'] = piano.topic + '/' + stanza.topic + '/' + attuatore.topic
                attuatoreObj['description'] = attuatore.description
                attuatoriArray.append(attuatoreObj)
            stanzaObj['attuatori'] = attuatoriArray
            stanzeArray.append(stanzaObj)
            attuatoriArray = []
        pianoObj['stanze'] = stanzeArray
        pianiArray.append(pianoObj)
        stanzeArray = []

    return pianiArray


# Restituisce l'elenco di tutti i topic associati ad attuatori di tipo lampada
def get_topics():
    piani = Piano.query.all()
    topicArray = []

    for piano in piani:
        stanze = Stanza.query.filter_by(piano_id=piano.id).all()
        for stanza in stanze:
        # Aggiungere elenco attuatori sia di tipo "lampada" che di tipo "serratura"
        # Da vedere come costruire la query con operatore di OR
            attuatori = Attuatore.query.filter_by(stanza_id=stanza.id, type='lampada')
            for attuatore in attuatori:
                topicObj = {}
                topicObj['id'] = attuatore.id
                topicObj['topic'] = piano.topic + '/' + stanza.topic + '/' + attuatore.topic
            topicArray.append(topicObj)

    return topicArray

def mqtt_publish(id, value):
    att = Attuatore.query.filter_by(id=id).first()
    stanza = Stanza.query.filter_by(id=att.stanza_id).first()
    topic = str(stanza.piano_id) + '/' + str(stanza.id) + '/' + str(id)
    client.publish(topic, value)
    return "OK"