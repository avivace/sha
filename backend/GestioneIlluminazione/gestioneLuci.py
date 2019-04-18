import time
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

dbPath = r'/home/pi/smart-home-automation/webapp/app.db'

engine = create_engine('sqlite:///%s' % dbPath, echo=False)
Base = declarative_base(engine)

class Piano(Base):
    """"""
    __tablename__ = 'piano'
    __table_args__ = {'autoload':True}

class Stanza(Base):
    """"""
    __tablename__ = 'stanza'
    __table_args__ = {'autoload':True}

class Attuatore(Base):
    """"""
    __tablename__ = 'attuatore'
    __table_args__ = {'autoload':True}

def loadSession():
    """"""
    metadata = Base.metadata
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

session = loadSession()

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

def loadHomeConfiguration():
    piani = session.query(Piano).all()
    attuatoreObj = {}

    for piano in piani:
        stanze = session.query(Stanza).filter_by(piano_id=piano.id).all()
        for stanza in stanze:
            attuatori = session.query(Attuatore).filter_by(stanza_id=stanza.id, type='lampada')
            for attuatore in attuatori:
                attuatoreObj[piano.topic + '/' + stanza.topic + '/' + attuatore.topic] = attuatore.pin

    return attuatoreObj

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print ("\nDISCONNESSO")

def on_connect(client, userdata, flags, rc):
    print ("CONNESSIONE EFFETTUATA\n")

    for topic in userdata:
        client.subscribe(topic)
        GPIO.setup(userdata[topic], GPIO.OUT)
        GPIO.output(userdata[topic], 1)
        print('Sottoscritto al topic: ' + topic)
    print('\n')

def on_message(client, userdata, msg):
      messaggio=str(msg.payload)
      topic=str(msg.topic)
      print ("RICEVUTO COMANDO: " + messaggio + " SUL TOPIC: " + topic)

      if userdata.has_key(topic):
         GPIO.output(userdata[topic], int(messaggio))
         client.publish("state/" + topic, messaggio)
         print ("NOTIFICA STATO: " + messaggio + " SUL TOPIC: " + "state/" + topic + "\n")

client = mqtt.Client(userdata=loadHomeConfiguration())
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

try:
    time.sleep(0.2)
    client.connect("192.168.1.14", 1883, 60)
except:
    print ("ERRORE MQTT")

client.loop_forever()