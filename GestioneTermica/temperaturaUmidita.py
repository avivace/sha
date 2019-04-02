# coding=utf-8
import Adafruit_DHT
import time
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Potrebbe essermi utile per generare un topic in caso di errore di lettura dal sensore
import paho.mqtt.client as mqtt

dbPath = r'/home/pi/Desktop/SmartHomeAutomationNV/app.db'

engine = create_engine('sqlite:///%s' % dbPath, echo=True)
Base = declarative_base(engine)

class Lettura(Base):
    """"""
    __tablename__ = 'lettura'
    __table_args__ = {'autoload':True}

class Sensore(Base):
    """"""
    __tablename__ = 'sensore'
    __table_args__ = {'autoload':True}

def loadSession():
    """"""
    metadata = Base.metadata
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

session = loadSession()

sensor = Adafruit_DHT.DHT22
sensori = session.query(Sensore).all()

while True:

    for sensore in sensori:
        humidity, temperature = Adafruit_DHT.read_retry(sensor, sensore.pin)
        if humidity is not None and temperature is not None:
            print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
            nuova_lettura=Lettura(timestamp=datetime.now(), temperatura=temperature, umidita=humidity, sensore_id=sensore.id)
        else:
            print('Lettura Fallita')
            sys.exit(1)

        # Dopo ogni lettura scrivo sul db le rilevazioni ottenute
        session.add(nuova_lettura)
        session.commit()
    time.sleep(60)