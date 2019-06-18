import time
import json
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import requests

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

def loadLuci():
    endpoint = "http://127.0.0.1:8081/auth"
    data = {}
    data['password'] = "7dab3e305e5526ac299576a9d23473f2fd003d43356ae9661ed205eb3a77eb47a842078f872c1784621a51eddd22915bb748e8772d795fc3687801e0f552a7dc"
    data['username'] = "marco"

    headers = {}
    headers['Content-type'] = "application/json"
    headers['Accept'] = "text/plain"

    response = requests.post(endpoint, data=json.dumps(data), headers=headers).json()
    token = response['token']

    endpoint = "http://127.0.0.1:8081/overview"
    headers = {}
    headers['Accept'] = "text/plain"
    headers['Authorization'] = "Bearer " + token

    response = requests.get(endpoint, headers=headers).json()

    attuatoreObj = {}
    for piano in response:
        for stanza in piano['stanze']:
             for attuatore in stanza['attuatori']:
                attuatoreObj[str(piano['id']) + '/' + str(stanza['id']) + '/' + str(attuatore['id'])] = attuatore['pin']

    return attuatoreObj

# Metodo eseguito in fase di disconnessione dal Broker MQTT
def on_disconnect(client, userdata, rc):
    if rc != 0:
        print ("\nDISCONNESSO")

# Metodo eseguito in fase collegamento al Broker MQTT
def on_connect(client, userdata, flags, rc):
    print ("CONNESSIONE EFFETTUATA\n")
    #Settaggio GPIO Raspberry
    for topic in userdata:
        client.subscribe(topic)
        print('Sottoscritto al topic: ' + topic + '\n')
        GPIO.setup(userdata[topic], GPIO.OUT)
        GPIO.output(userdata[topic], 1)

# Metodo eseguito alla ricezione di un messaggio MQTT
def on_message(client, userdata, msg):
    messaggio=str(msg.payload)
    topic=str(msg.topic)
    print ("RICEVUTO COMANDO: " + messaggio + " SUL TOPIC: " + topic)

    if topic in userdata:
        GPIO.output(userdata[topic], int(messaggio))

print("ASSOCIAZIONE TOPIC-PIN:\n")
print(loadLuci())
print("\n")

client = mqtt.Client(userdata=loadLuci())
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

try:
    time.sleep(0.2)
    client.connect("127.0.0.1", 1883, 60)
    topic = "notifica/controlloreLuci"
    client.publish(topic, "OK")
except:
    print ("ERRORE MQTT")

client.loop_forever()