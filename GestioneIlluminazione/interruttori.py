import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
attesa_pulsante=0.05

# DICHIARAZIONE GPIO INTERRUTTORI
int_uno = 5
#int_due = da collegare
#int_tre = da collegare
#int_qua = da collegare

GPIO.setup(int_uno,  GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setup(int_due,  GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setup(int_tre,  GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setup(int_qua,  GPIO.IN, pull_up_down=GPIO.PUD_UP)


# ANALISI E DICHIARAZIONE DELLO STATO INIZIALE DEGLI INTERRUTTORI
stato_int_uno=GPIO.input(int_uno)
#stato_int_due=GPIO.input(int_due)
#stato_int_tre=GPIO.input(int_tre)
#stato_int_qua=GPIO.input(int_qua)

# DICHIARAZIONE GPIO LUCI
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

# SPENGO TUTTE LE LUCI ALL'AVVIO
GPIO.output(luce_uno, 1)
GPIO.output(luce_due, 1)
GPIO.output(luce_tre, 1)
GPIO.output(luce_qua, 1)
GPIO.output(luce_cin, 1)
GPIO.output(luce_sei, 1)
GPIO.output(luce_set, 1)
GPIO.output(luce_ott, 1)

# AZZERO ANCHE LO STATO DEGLI INTERRUTTORI SULL'INTERFACCIA

try:
    client = mqtt.Client()
    client.connect("192.168.1.14", 1883, 60)
    topic = "notifica/controlloreInterruttori"
    client.publish(topic, "OK")
except:
    print ("ERRORE MQTT")
	
client.publish("state/pianoTerra/cucina/lampadario", 1)
client.publish("state/pianoTerra/bagno/lampadario", 1)
client.publish("state/pianoTerra/salotto/lampadario", 1)
client.publish("state/primoPiano/cameraMatrimoniale/lampadario", 1)
client.publish("state/primoPiano/bagno/lampadario", 1)
client.publish("state/mansarda/bagno/lampadario", 1)
client.publish("state/garage/lavanderia/lampadario", 1)

while True:

    # CONTROLLO INTERRUTTORE 1
    if GPIO.input(int_uno) == 0 and stato_int_uno != 0:
        stato_rele_uno=GPIO.input(luce_uno)
        stato_int_uno=GPIO.input(int_uno)
        if stato_rele_uno==1: stato_rele_uno=0
        elif stato_rele_uno==0: stato_rele_uno=1

        GPIO.output(luce_uno, stato_rele_uno)
        topic = "state/pianoTerra/cucina/lampadario"
        client.publish(topic, stato_rele_uno)

        print ("COMANDO: " + str(stato_rele_uno) + " TOPIC: " + topic)
        print ("LUCE UNO: " + str(stato_rele_uno))
	
    if GPIO.input(int_uno) == 1 and stato_int_uno != 1:
        stato_int_uno = 1

    # CONTROLLO INTERRUTTORE 2
    #if GPIO.input(int_due) != stato_int_due:
     #   stato_rele_due=GPIO.input(luce_due)
      #  stato_int_due=GPIO.input(int_due)
       # if stato_rele_due==1: stato_rele_due=0
        #elif stato_rele_due==0: stato_rele_due=1

        #GPIO.output(luce_due, stato_rele_due)
        #client = mqtt.Client()
        #try:
         #   client.connect("192.168.1.14", 1883, 60)
          #  topic = "prova/state/salotto/luce_due"
           # client.publish(topic, stato_rele_due)
            #print "invio " + str(stato_rele_due) + " al topic " + topic
        #except:
         #   print "errore MQTT"
        #print " luce due " + str(stato_rele_due)

    time.sleep(attesa_pulsante)