import time
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Percorso al Database SQLite
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

class Pulsante(Base):
    """"""
    __tablename__ = 'pulsante'
    __table_args__ = {'autoload':True}

def loadSession():
    """"""
    metadata = Base.metadata
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

# Restituisce l'elenco dei pulsanti memorizzati nel sistema
def loadPulsanti():
    piani = session.query(Piano).all()
    pulsantiArray = []

    for piano in piani:
        stanze = session.query(Stanza).filter_by(piano_id=piano.id).all()
        for stanza in stanze:
            attuatori = session.query(Attuatore).filter_by(stanza_id=stanza.id)
            for attuatore in attuatori:
                pulsanti = session.query(Pulsante).filter_by(attuatore_id=attuatore.id)
                for pulsante in pulsanti:
                    pulsanteObj = {}
                    pulsanteObj['tipo'] = attuatore.type
                    pulsanteObj['pin_attuatore'] = attuatore.pin
                    pulsanteObj['topic'] = piano.topic + '/' + stanza.topic + '/' + attuatore.topic
                    pulsanteObj['pin_pulsante'] = pulsante.pin
                    pulsantiArray.append(pulsanteObj)

    return pulsantiArray

session = loadSession()
pulsanti = loadPulsanti()

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

attesa_pulsante=0.05

# Settaggio GPIO Raspberry
for pulsante in pulsanti:
    GPIO.setup(pulsante['pin_pulsante'],  GPIO.IN, pull_up_down=GPIO.PUD_UP)
    pulsante['stato_pulsante'] = GPIO.input(pulsante['pin_pulsante'])
    GPIO.setup(pulsante['pin_attuatore'], GPIO.OUT)
    GPIO.output(pulsante['pin_attuatore'], 1)

# Effettuo la connessione a Broker MQTT
try:
    client = mqtt.Client()
    client.connect("192.168.1.14", 1883, 60)
    topic = "notifica/controlloreInterruttori"
    client.publish(topic, "OK")
except:
    print ("ERRORE MQTT")

# All'avvio spengo tutti i dispositivi connessi ai pulsanti
for pulsante in pulsanti:
    client.connect("192.168.1.14", 1883, 60)
    client.publish('state/' + pulsante['topic'], 1)

# Controllo ciclico sui pulsanti memorizzati nel sistema
while True:
    # Da aggiungere la gestione diversificate di pulsanti per luci e per serrature
    for pulsante in pulsanti:
        if GPIO.input(pulsante['pin_pulsante']) == 0 and pulsante['stato_pulsante'] != 0:
            stato_rele = GPIO.input(pulsante['pin_attuatore'])
            pulsante['stato_pulsante'] = GPIO.input(pulsante['pin_pulsante'])
            if stato_rele == 1: stato_rele = 0
            elif stato_rele == 0: stato_rele = 1

            print ("COMANDO: " + str(GPIO.input(pulsante['pin_pulsante'])) + "\nSU TOPIC: " + pulsante['topic'] + "\nATTUATORE PRIMA: " + str(GPIO.input(pulsante['pin_attuatore'])))

            GPIO.output(pulsante['pin_attuatore'], stato_rele)
            client.connect("192.168.1.14", 1883, 60)
            client.publish('state/' + pulsante['topic'], stato_rele)

            print ("ATTUATORE DOPO: " + str(GPIO.input(pulsante['pin_attuatore'])) + '\n')

        if GPIO.input(pulsante['pin_pulsante']) == 1 and pulsante['stato_pulsante'] != 1:
            pulsante['stato_pulsante'] = 1

    time.sleep(attesa_pulsante)