from datetime import datetime, timedelta
import unittest
from app import db
from models import User, hash_password
from config import Config
import requests
import json
	
class UserCase(unittest.TestCase):

    # Test codifica password
    def test_password_hashing(self):
        u = User(username='susan')
        u.set_password('cat')
        self.assertFalse(u.check_password(hash_password('dog')))
        self.assertTrue(u.check_password(hash_password('cat')))

    # Test avatar utente
    def test_avatar(self):
        u = User(username='john', email='john@example.com')
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/'
                                         'd4c74594d841139328695756648b6bd6'
                                         '?d=identicon&s=128'))		
        
    # Test autenticazione con username e password(codificata) e verifica validità token ricevuto
    def test_auth_token_correct(self):
        # Richiesta token di autenticazione
        endpoint = "http://127.0.0.1:8081/auth"
        data = {}
        data['password'] = "7dab3e305e5526ac299576a9d23473f2fd003d43356ae9661ed205eb3a77eb47a842078f872c1784621a51eddd22915bb748e8772d795fc3687801e0f552a7dc"
        data['username'] = "marco"
        
        headers = {}
        headers['Content-type'] = "application/json"
        headers['Accept'] = "text/plain"
        
        response = requests.post(endpoint, data=json.dumps(data), headers=headers)
        self.assertEqual(response.status_code, 200)
        response = response.json()
        token = response['token']
        
        #Verifica correttezza del token ricevuto
        endpoint = "http://127.0.0.1:8081/verify-token"
        headers = {}
        headers['Accept'] = "text/plain"
        headers['Authorization'] = "Bearer " + token

        response = requests.get(endpoint, headers=headers)
        self.assertEqual(response.status_code, 200)
    
    # Test autenticazione con username e password(codificata) e verifica fallimento token errato
    def test_auth_token_uncorrect(self):
        # Richiesta token di autenticazione
        endpoint = "http://127.0.0.1:8081/auth"
        data = {}
        data['password'] = "7dab3e305e5526ac299576a9d23473f2fd003d43356ae9661ed205eb3a77eb47a842078f872c1784621a51eddd22915bb748e8772d795fc3687801e0f552a7dc"
        data['username'] = "marco"
        
        headers = {}
        headers['Content-type'] = "application/json"
        headers['Accept'] = "text/plain"
        
        response = requests.post(endpoint, data=json.dumps(data), headers=headers)
        self.assertEqual(response.status_code, 200)
        response = response.json()
        token = response['token']
        
        #Verifica correttezza del token ricevuto
        endpoint = "http://127.0.0.1:8081/verify-token"
        headers = {}
        headers['Accept'] = "text/plain"
        headers['Authorization'] = "Bearer " + "TokenErrato"

        response = requests.get(endpoint, headers=headers)
        self.assertEqual(response.status_code, 500)
   
class HomeConfigurationCase(unittest.TestCase):
    
    # Aggiunta di un nuovo piano (Scenario di successo)
    def test_aggiungi_piano_correct(self):
        # Richiesta token di autenticazione
        endpoint = "http://127.0.0.1:8081/auth"
        data = {}
        data['password'] = "7dab3e305e5526ac299576a9d23473f2fd003d43356ae9661ed205eb3a77eb47a842078f872c1784621a51eddd22915bb748e8772d795fc3687801e0f552a7dc"
        data['username'] = "marco"
        
        headers = {}
        headers['Content-type'] = "application/json"
        headers['Accept'] = "text/plain"
        
        response = requests.post(endpoint, data=json.dumps(data), headers=headers)
        self.assertEqual(response.status_code, 200)
        response = response.json()
        token = response['token']
        
        #Aggiunta di un nuovo piano
        endpoint = "http://127.0.0.1:8081/add-piano"
        data = {}
        data['description'] = "Piano Terra"
        
        headers = {}
        headers['Content-type'] = "application/json"
        headers['Accept'] = "text/plain"
        headers['Authorization'] = "Bearer " + token

        response = requests.post(endpoint, data=json.dumps(data), headers=headers)
        self.assertEqual(response.status_code, 200)  
        
    #Aggiunta di un nuovo piano (Scenario di fallimento)
    def test_aggiungi_piano_uncorrect(self):
        # Richiesta token di autenticazione
        endpoint = "http://127.0.0.1:8081/auth"
        data = {}
        data['password'] = "7dab3e305e5526ac299576a9d23473f2fd003d43356ae9661ed205eb3a77eb47a842078f872c1784621a51eddd22915bb748e8772d795fc3687801e0f552a7dc"
        data['username'] = "marco"
        
        headers = {}
        headers['Content-type'] = "application/json"
        headers['Accept'] = "text/plain"
        
        response = requests.post(endpoint, data=json.dumps(data), headers=headers)
        self.assertEqual(response.status_code, 200)
        response = response.json()
        token = response['token']
        
        #Aggiunta di un nuovo piano
        endpoint = "http://127.0.0.1:8081/add-piano"
        data = {}
        data['description'] = 3 # Specifico un numero anzichè una stringa di testo
        
        headers = {}
        headers['Content-type'] = "application/json"
        headers['Accept'] = "text/plain"
        headers['Authorization'] = "Bearer " + token

        response = requests.post(endpoint, data=json.dumps(data), headers=headers)
        self.assertEqual(response.status_code, 400) 
        
    # Aggiunta di una nuova stanza (Scenario di successo)
    def test_aggiungi_stanza_correct(self):
        # Richiesta token di autenticazione
        endpoint = "http://127.0.0.1:8081/auth"
        data = {}
        data['password'] = "7dab3e305e5526ac299576a9d23473f2fd003d43356ae9661ed205eb3a77eb47a842078f872c1784621a51eddd22915bb748e8772d795fc3687801e0f552a7dc"
        data['username'] = "marco"
        
        headers = {}
        headers['Content-type'] = "application/json"
        headers['Accept'] = "text/plain"
        
        response = requests.post(endpoint, data=json.dumps(data), headers=headers)
        self.assertEqual(response.status_code, 200)
        response = response.json()
        token = response['token']
        
        #Aggiunta di una nuova stanza
        endpoint = "http://127.0.0.1:8081/add-stanza"
        data = {}
        data['description'] = "Cucina"
        data['piano_id'] = 1
        
        headers = {}
        headers['Content-type'] = "application/json"
        headers['Accept'] = "text/plain"
        headers['Authorization'] = "Bearer " + token

        response = requests.post(endpoint, data=json.dumps(data), headers=headers)
        self.assertEqual(response.status_code, 200)  
        
    #Aggiunta di un nuova stanza (Scenario di fallimento)
    def test_aggiungi_stanza_uncorrect(self):
        # Richiesta token di autenticazione
        endpoint = "http://127.0.0.1:8081/auth"
        data = {}
        data['password'] = "7dab3e305e5526ac299576a9d23473f2fd003d43356ae9661ed205eb3a77eb47a842078f872c1784621a51eddd22915bb748e8772d795fc3687801e0f552a7dc"
        data['username'] = "marco"
        
        headers = {}
        headers['Content-type'] = "application/json"
        headers['Accept'] = "text/plain"
        
        response = requests.post(endpoint, data=json.dumps(data), headers=headers)
        self.assertEqual(response.status_code, 200)
        response = response.json()
        token = response['token']
        
        #Aggiunta di una nuova stanza
        endpoint = "http://127.0.0.1:8081/add-stanza"
        data = {}
        data['description'] = 3 # Specifico un numero anzichè una stringa di testo
        data['piano_id'] = 0 # Piano non esistente nel DB
        
        headers = {}
        headers['Content-type'] = "application/json"
        headers['Accept'] = "text/plain"
        headers['Authorization'] = "Bearer " + token

        response = requests.post(endpoint, data=json.dumps(data), headers=headers)
        self.assertEqual(response.status_code, 400)
        
    # Aggiunta di un nuovo dispositivo (Scenario di successo)
    def test_aggiungi_dispositivo_correct(self):
        # Richiesta token di autenticazione
        endpoint = "http://127.0.0.1:8081/auth"
        data = {}
        data['password'] = "7dab3e305e5526ac299576a9d23473f2fd003d43356ae9661ed205eb3a77eb47a842078f872c1784621a51eddd22915bb748e8772d795fc3687801e0f552a7dc"
        data['username'] = "marco"
        
        headers = {}
        headers['Content-type'] = "application/json"
        headers['Accept'] = "text/plain"
        
        response = requests.post(endpoint, data=json.dumps(data), headers=headers)
        self.assertEqual(response.status_code, 200)
        response = response.json()
        token = response['token']
        
        #Aggiunta di un nuovo dispositivo
        endpoint = "http://127.0.0.1:8081/add-device"
        data = {}
        data['description'] = "Lampadario"
        data['pin'] = 1001
        data['stanza_id'] = 1
        data['topic'] = "luce" 
        data['type'] = "lampada"
        
        headers = {}
        headers['Content-type'] = "application/json"
        headers['Accept'] = "text/plain"
        headers['Authorization'] = "Bearer " + token
        
        response = requests.post(endpoint, data=json.dumps(data), headers=headers)
        self.assertEqual(response.status_code, 200)  
        
    #Aggiunta di un nuovo dispositivo (Scenario di fallimento)
    def test_aggiungi_dispositivo_uncorrect(self):
        # Richiesta token di autenticazione
        endpoint = "http://127.0.0.1:8081/auth"
        data = {}
        data['password'] = "7dab3e305e5526ac299576a9d23473f2fd003d43356ae9661ed205eb3a77eb47a842078f872c1784621a51eddd22915bb748e8772d795fc3687801e0f552a7dc"
        data['username'] = "marco"
        
        headers = {}
        headers['Content-type'] = "application/json"
        headers['Accept'] = "text/plain"
        
        response = requests.post(endpoint, data=json.dumps(data), headers=headers)
        self.assertEqual(response.status_code, 200)
        response = response.json()
        token = response['token']
        
        #Aggiunta di un nuovo dispositivo
        endpoint = "http://127.0.0.1:8081/add-device"
        data = {}
        data['description'] = "Lampadario"
        data['pin'] = 1001 # Due dispositivi connessi allo stesso pin viola vincolo di chiave DB
        data['stanza_id'] = 1
        data['topic'] = "luce" 
        data['type'] = "lampada"
        
        headers = {}
        headers['Content-type'] = "application/json"
        headers['Accept'] = "text/plain"
        headers['Authorization'] = "Bearer " + token

        response = requests.post(endpoint, data=json.dumps(data), headers=headers)
        self.assertEqual(response.status_code, 500)
    
    # Richiesta elenco topic memorizzati
    def test_get_topics(self):
        # Richiesta token di autenticazione
        endpoint = "http://127.0.0.1:8081/auth"
        data = {}
        data['password'] = "7dab3e305e5526ac299576a9d23473f2fd003d43356ae9661ed205eb3a77eb47a842078f872c1784621a51eddd22915bb748e8772d795fc3687801e0f552a7dc"
        data['username'] = "marco"
        
        headers = {}
        headers['Content-type'] = "application/json"
        headers['Accept'] = "text/plain"
        
        response = requests.post(endpoint, data=json.dumps(data), headers=headers)
        self.assertEqual(response.status_code, 200)
        response = response.json()
        token = response['token']
        
        #Richiede elenco dei topic
        endpoint = "http://127.0.0.1:8081/get-topics"
        headers = {}
        headers['Accept'] = "text/plain"
        headers['Authorization'] = "Bearer " + token

        response = requests.get(endpoint, headers=headers)
        #print(response.json())
        self.assertEqual(response.status_code, 200)
    
    # Richiesta configurazione abitazione
    def test_overview(self):
        # Richiesta token di autenticazione
        endpoint = "http://127.0.0.1:8081/auth"
        data = {}
        data['password'] = "7dab3e305e5526ac299576a9d23473f2fd003d43356ae9661ed205eb3a77eb47a842078f872c1784621a51eddd22915bb748e8772d795fc3687801e0f552a7dc"
        data['username'] = "marco"
        
        headers = {}
        headers['Content-type'] = "application/json"
        headers['Accept'] = "text/plain"
        
        response = requests.post(endpoint, data=json.dumps(data), headers=headers)
        self.assertEqual(response.status_code, 200)
        response = response.json()
        token = response['token']
        
        #Richiesta organizzazione in piani, stanze e attuatori
        endpoint = "http://127.0.0.1:8081/overview"
        headers = {}
        headers['Accept'] = "text/plain"
        headers['Authorization'] = "Bearer " + token

        response = requests.get(endpoint, headers=headers)
        #print(response.json())
        self.assertEqual(response.status_code, 200)     
        
        # Richiesta configurazione abitazione
    def test_richiesta_cambio_stato_attuatore(self):
        # Richiesta token di autenticazione
        endpoint = "http://127.0.0.1:8081/auth"
        data = {}
        data['password'] = "7dab3e305e5526ac299576a9d23473f2fd003d43356ae9661ed205eb3a77eb47a842078f872c1784621a51eddd22915bb748e8772d795fc3687801e0f552a7dc"
        data['username'] = "marco"
        
        headers = {}
        headers['Content-type'] = "application/json"
        headers['Accept'] = "text/plain"
        
        response = requests.post(endpoint, data=json.dumps(data), headers=headers)
        self.assertEqual(response.status_code, 200)
        response = response.json()
        token = response['token']
        
        #Richiesta cambio stato attuatore, garanzia di invio richiesta
        endpoint = "http://127.0.0.1:8081/publish/1/1"
        headers = {}
        headers['Accept'] = "text/plain"
        headers['Authorization'] = "Bearer " + token

        response = requests.get(endpoint, headers=headers)
        self.assertEqual(response.status_code, 200) 
        
if __name__ == '__main__':
    unittest.main(verbosity=2)
    token = ""