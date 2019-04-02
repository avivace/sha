import paho.mqtt.client as mqtt
import time
import RPi.GPIO as GPIO
from datetime import datetime

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

luce_uno=6
luce_due=13
luce_tre=19
luce_qua=26
luce_cin=12
luce_sei=16
luce_set=20
luce_ott=21

GPIO.setup(luce_uno, GPIO.OUT)
GPIO.setup(luce_due, GPIO.OUT)
GPIO.setup(luce_tre, GPIO.OUT)
GPIO.setup(luce_qua, GPIO.OUT)
GPIO.setup(luce_cin, GPIO.OUT)
GPIO.setup(luce_sei, GPIO.OUT)
GPIO.setup(luce_set, GPIO.OUT)
GPIO.setup(luce_ott, GPIO.OUT)

def on_disconnect(client, userdata, rc):
    if rc != 0:
        adesso=time.time()
        fh=open("/home/pi/luci/log.txt",'r')
        leggi=fh.readlines()
        fh.close()
        fh=open("/home/pi/luci/log.txt",'w')
        fh.writelines(leggi)
        ora_log=(time.strftime("%H:%M:%S %d/%m/%Y"))
        fh.write('MQTT disconnesso ' + ora_log + ' ' + '\n')
        fh.close()
        print (" disconnesso dal server")

def on_connect(client, userdata, flags, rc):
    print ("CONNESSO")
    client.subscribe("pianoTerra/cucina/lampadario")
    client.subscribe("pianoTerra/bagno/lampadario")
    client.subscribe("pianoTerra/salotto/lampadario")
    client.subscribe("primoPiano/cameraMatrimoniale/lampadario")
    client.subscribe("primoPiano/bagno/lampadario")
    client.subscribe("mansarda/bagno/lampadario")
    client.subscribe("garage/lavanderia/lampadario")

def on_message(client, userdata, msg):
      messaggio=str(msg.payload)
      topic=str(msg.topic)
      print ("COMANDO: " + messaggio + " TOPIC: " + topic)

      if topic=="pianoTerra/cucina/lampadario":
         if messaggio=="1" or messaggio=="0":
             GPIO.output(luce_uno, int(messaggio))
             client.publish("state/pianoTerra/cucina/lampadario", messaggio)
             print ("LUCE UNO: " + messaggio)

      if topic=="pianoTerra/bagno/lampadario":
         if messaggio=="1" or messaggio=="0":
             GPIO.output(luce_due, int(messaggio))
             client.publish("state/pianoTerra/bagno/lampadario", messaggio)
             print ("LUCE DUE: " + messaggio)

      if topic=="pianoTerra/salotto/lampadario":
         if messaggio=="1" or messaggio=="0":
             GPIO.output(luce_tre, int(messaggio))
             client.publish("state/pianoTerra/salotto/lampadario", messaggio)
             print ("LUCE TRE: " + messaggio)

      if topic=="primoPiano/cameraMatrimoniale/lampadario":
         if messaggio=="1" or messaggio=="0":
             GPIO.output(luce_qua, int(messaggio))
             client.publish("state/primoPiano/cameraMatrimoniale/lampadario", messaggio)
             print ("LUCE QUATTRO: " + messaggio)

      if topic=="primoPiano/bagno/lampadario":
         if messaggio=="1" or messaggio=="0":
             GPIO.output(luce_cin, int(messaggio))
             client.publish("state/primoPiano/bagno/lampadario", messaggio)
             print ("LUCE CINQUE: " + messaggio)

      if topic=="mansarda/bagno/lampadario":
         if messaggio=="1" or messaggio=="0":
             GPIO.output(luce_sei, int(messaggio))
             client.publish("state/mansarda/bagno/lampadario", messaggio)
             print ("LUCE SEI: " + messaggio)

      if topic=="garage/lavanderia/lampadario":
         if messaggio=="1" or messaggio=="0":
             GPIO.output(luce_set, int(messaggio))
             client.publish("state/garage/lavanderia/lampadario", messaggio)
             print ("LUCE SETTE: " + messaggio)

GPIO.output(luce_uno, 1)
GPIO.output(luce_due, 1)
GPIO.output(luce_tre, 1)
GPIO.output(luce_qua, 1)
GPIO.output(luce_cin, 1)
GPIO.output(luce_sei, 1)
GPIO.output(luce_set, 1)
GPIO.output(luce_ott, 1)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

try:
    time.sleep(0.2)
    client.connect("192.168.1.14", 1883, 60)
except:
    print ("ERRORE MQTT")

client.loop_forever()
