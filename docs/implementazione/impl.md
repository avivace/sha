# Smart Home Automation - Implementazione

> Marco Belotti, Francesco Bombarda, Antonio Vivace.

Questo documento fornisce una panoramica del software realizzato per implementare le funzionalità del sistema SHA.

Chiariremo qual è il sottoinsieme di funzionalità che abbiamo deciso di implementare nel software finale.

Verranno introdotti e contestualizzati i vari strumenti, librerie software, tecniche e pattern utilizzati specificandone gli standard e le norme industriali che li descrivono.

Particolare rilevanza è stata data al modo in cui ognuno dei diversi strumenti copre il proprio ruolo e come essi vengono incastonati nel sistema che realizza un intero stack web.

Infine, verrà spiegato brevemente come preparare un sistema UNIX all'esecuzione di ognuna delle componenti del software stesso, preoccupandosi di soddisfare i prerequisiti, di installare automaticamente gli ambienti che provvedano a tutte le dipendenze ed infine eseguire ed esporre i servizi finali.

## Funzionalità implementate

Rispetto ai requisiti e all'architettura descritti negli altri documenti, abbiamo deciso di implementare un sotto insieme significativo di questi ultimi. In generale, sono state implementate le funzionalità che potessero permettere ai casi d'uso principali di funzionare.
Il software fornisce un framework solido su cui, eventualmente, preparare e aggiungere le nuove caratteristiche, oppure espandere quelle esistenti.

In particolare:

## Backend

- Tutte le funzionalità sono esposte come API Restful, definite formalmente con uno schema OpenAPI 3.
  + I parametri della richiesta e le risposte sono sempre validati formalmente con altrettanti schema.
  + Tutte le risposte serializzate in JSON.
  + L'API è agnostica e sfruttabile da qualsiasi libreria o ambiente di sviluppo dotato di un client HTTP.
  + Viene generata una documentazione dinamica di ognuna delle funzionalità esposte dall'API, mostrando come utilizzare e cosa aspettarsi da ognuna delle funzionalità.
- Esposizione dello stato dei punti luce e modifica degli stessi tramite MQTT.
- Sistema di autenticazione completo basato su JWT. Permette:
  + login, 
  + logout, 
  + gestione di sessione, 
  + registrazione,
  + recupero credenziali,
  + fare richieste/ricevere risposte autenticate e firmate.
- Diversi livelli di utenza.
- L'intero stato della configurazione è in un database SQLite di cui si possono facilmente fare snapshot periodici, esportarli ed importarli.

Sono infine state create classi per poter sfruttare un mailer e gestire anche l'invio di email secondo template per notifiche e recupero dell'account.

### API

### Panoramica degli strumenti

#### MQTT

TODO

- [ISO/IEC PRF 20922](https://webstore.iec.ch/preview/info_isoiec20922%7Bed1.0%7Den.pdf)

#### JWT

I JWT sono degli oggetti (tokens) che permettono di inviare dati ad un server usando il formato JSON. Questo è molto utile per creare un sistema di autenticazione user stateless.

L’autenticazione dell’user e la gestione delle sessioni, vengono quasi sempre fatte attraverso l’uso dei Cookies. Il processo di login con un sistema basato sui cookies di solito è basato su quattro passaggi:

- Cliente invia dettagli di login
- Server risponde con il cookie ed il session ID
- Cliente ri-invia il cookie quando richiede una nuova pagina
- Server effettua un controllo sul cookie e accetta / rifiuta la connessione

Con l’uso dei JSON Web Tokens il processo è molto simile ma con alcune differenze:

Anche con i JWT, quando il client effettua il login correttamente il server gli invia in risposta un token. Questo token viene salvato nel local storage ed inviato al server che effettuerà i controlli necessari e risponderà.

La differenza principale è che con l’utilizzo delle sessions, il server ha bisogno di salvare i dati relativi ai suoi user in memoria. Nel caso dei JWT invece tutti i dati necessari sono contenuti nel token stesso, rendendo il server stateless. 

Questo ci può tornare molto utile quando stiamo sviluppando applicazioni a singola pagina, dove il codice client è completamente indipendente dal codice server.

- [RFC 7515](https://tools.ietf.org/html/rfc7515) - JSON Web Signature (JWS)
- [RFC 7516](https://tools.ietf.org/html/rfc7516) - JSON Web Encryption (JWE)
- [RFC 7519](https://tools.ietf.org/html/rfc7519) - JSON Web Token (JWT)

Una volta ottenuto e validato un token che certifica la nostra "rivendicazione" di essere un dato utente, basterà consumare ogni rotta che richiede l'autenticazione (segnata con un lucchetto sulla nostra documentazione) aggiungendo un HEADER al pacchetto HTTP che include il nostro token.

Esempio:

```bash
curl -X GET "http://localhost:8080/secret" -H  "accept: text/plain" -H
 "Authorization: Bearer $TOKEN"
```

#### Open API 3.0

La Specifica OpenAPI (conosciuta originariamente come la Specifica Swagger) è una specifica per file di interfaccia leggibili dalle macchine per descrivere, produrre, consumare e visualizzare servizi web RESTful.

Una serie di strumenti può generare codice, documentazione e test case dato un file di interfaccia.

- [OpenAPI Specification, version 3.0.0](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md)

#### Flask

Flask è un framework web leggero scritto in Python e basato sullo strumento Werkzeug WSGI e con il motore template Jinja2. Ha licenza BSD.

Flask è un microframework perché ha un nucleo semplice ma estensibile. Non c'è uno strato di astrazione per la base di dati, validazione delle form, o qualsiasi altra componente dove esistono già librerie di terze parti per fornire funzionalità comuni (per cui noi usiamo Connexion per le validazioni delle rotte e SQL Alchemy come driver ed ORM per SQLite) Sebbene, Flask supporti estensioni, che possono aggiungere funzionalità ad un'applicazione come era implementato in Flask stesso. Ci sono estensioni per mappatori ad oggetti-relazionali, gestione del caricamento, e varie tecnologie di autenticazione e altro. 

#### Connexion

Connexion è un "wrapper"

È un ambiente completo per implementare delle applicazioni che espongono un API definita con standard OpenAPI. Fornisce un'interfaccia che autodocumenta le rotte descritte e permette di testarle ed utilizzarle durante lo sviluppo.

Dato che ogni rotta è formalmente definita, e specifica che tipo di oggetti deve ricevere (Query param, URL templatizzate, JSON payloads), procede in autonomia alla loro valutazioni, sollevano opportune eccezioni in caso di fallito casting ai tipi desiderati, parametri mancanti o malformati, od in generale quando la richiesta non viene costruita come precedentemente definito.

#### SQLite

SQLite è una libreria software scritta in linguaggio C che implementa un DBMS SQL di tipo ACID incorporabile all'interno di applicazioni. Non è un processo standalone utilizzabile di per sé, ma può essere incorporato all'interno di un altro programma.

#### SQLAlchemy

SQLAlchemy ci permette di utilizzare un database SQLite e fa da ORM, fornendo utili metodi e classi per definire i modelli del database ed operarci, senza dover necessariamente scrivere query SQL.

## Frontend

È un'applicazione in VueJS che implementa un'interfaccia utente facile ed immediata, implementando le funzionalità di controllo del sistema e di autenticazione sfruttando alcune delle rotte messe a disposizione dalla nostra API.

- Applicazione reattiva,
- Visualizzazione dello stato del sistema in tempo reale,
- Modifica di ogni punto luce del sistema,
- Funzionante su qualsiasi dispositivo dotato di un browser web.
- Possibilità di trasformarla facilmente in PWA con notifiche in tempo reale sul dispositivo, anche ad app web "chiusa".
 
### Panoramica degli strumenti

#### Node.js

Node.js è una runtime di JavaScript Open source.
Non è necessaria per eseguire la nostra applicazione frontend, che è completamente client side, ma viene utilizzato durante lo sviluppo per poter usare moduli JS diversi, unirli con webpack ed avviare un server web di prova che serve una build della nostra applicazione web.

In ogni caso, essa è completamente statica ed ottiene tutti i dati consumando con Axios l'API che abbiamo costruita.


#### Webpack

TODO

#### Vue.JS

TODO

#### Axios

TODO

#### Bootstrap-Vue

TODO

## Deploy del software

### MQTT

Requisiti iniziali, MQTT e Mosquitto.

Su Debian:

```bash
apt install mqtt mqtt-clients
service mqtt stop
mqtt
mosquitto_sub -h '127.0.0.1' -t '#'
```

### Backend

Requisiti iniziali.

Su Debian:
```
apt install python3 python3-pip python3-venv
```

Prepariamo l'ambiente e avviamo il backend
```bash
cd backend
python3 -m venv .
source bin/activate
pip3 install -r requirements.txt
pip3 install connexion[swagger-ui]
python3 app.py
```

### Frontend

Installare i requisiti iniziali (Node.js ed npm).

Su Debian:
```bash
curl -sL https://deb.nodesource.com/setup_12.x | bash -
apt-get install -y nodejs
```

```bash
cd frontend
npm install
npm run serve
```