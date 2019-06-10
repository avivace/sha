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

#### Backend

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
- L'intero stato della configurazione è serializzato in un database SQLite di cui si possono facilmente fare snapshot periodici, esportarli ed importarli.

#### Frontend

- Applicazione reattiva,
- Visualizzazione dello stato del sistema in tempo reale,
- Modifica di ogni punto luce del sistema,
- Funzionante su qualsiasi dispositivo dotato di un browser web.
- Possibilità di trasformarla facilmente in PWA con notifiche in tempo reale sul dispositivo, anche ad app web "chiusa".
 

## Panoramica degli strumenti

## Deploy del software
