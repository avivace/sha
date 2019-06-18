# Smart Home Automation
Documentazione e specifica OpenAPI 3 dell'API esposta da SHA.

## Version: 1.0

### /auth

#### POST
##### Summary:

Autentica l'utente con le credenziali fornite, fornendo un JWT token

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | JWT token |

### /requestPasswordReset

#### POST
##### Summary:

Richiedi il ripristino delle credenziali per l'utente con la mail o cellulare forniti

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Esito |

### /resetPassword/{resetToken}

#### POST
##### Summary:

Consuma il token per ripristinare la password

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| resetToken | path | Reset token | Yes | string |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Esito |

### /delete/{objtype}/{id}

#### DELETE
##### Summary:

Elimina un'entità (Piano, Stanza o Attuatore) dalla configurazione del sistema

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| id | path | ID | Yes | string |
| objtype | path | Tipo | Yes | string |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Response |

##### Security

| Security Schema | Scopes |
| --- | --- |
| jwt | secret |

### /get-topics

#### GET
##### Summary:

Restituisce l'elenco di tutti i topic associati ad attuaturi del tipo specificato

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Response |

##### Security

| Security Schema | Scopes |
| --- | --- |
| jwt | secret |

### /publish/{id}/{value}

#### POST
##### Summary:

Pubblica il valore specificato sul topic MQTT corrispondente all'ID fornito

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| id | path | ID attuatore | Yes | string |
| value | path | Valore | Yes | string |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Esito |

##### Security

| Security Schema | Scopes |
| --- | --- |
| jwt | secret |

### /overview

#### GET
##### Summary:

Ottieni una serializzazione JSON completa della configurazione del sistema in ogni sua parte

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Response |

##### Security

| Security Schema | Scopes |
| --- | --- |
| jwt | secret |

### /activate-user/{user_id}

#### PUT
##### Summary:

Attiva l'account specificato (da utente amministratore)

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| user_id | path | ID dell'utente da attivare | Yes | string |

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Esito |

##### Security

| Security Schema | Scopes |
| --- | --- |
| jwt | secret |

### /update-device

#### PUT
##### Summary:

Modifica i dettagli di un attuatore

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Outcome |

##### Security

| Security Schema | Scopes |
| --- | --- |
| jwt | secret |

### /add-device

#### POST
##### Summary:

Aggiungi un attuatore alla configurazione di sistema

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Outcome |

##### Security

| Security Schema | Scopes |
| --- | --- |
| jwt | secret |

### /add-stanza

#### POST
##### Summary:

Aggiungi una stanza alla configurazione di sistema

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Esito |

##### Security

| Security Schema | Scopes |
| --- | --- |
| jwt | secret |

### /add-piano

#### POST
##### Summary:

Aggiungi un piano alla configurazione di sistema

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Esito |

##### Security

| Security Schema | Scopes |
| --- | --- |
| jwt | secret |

### /verify-token

#### GET
##### Summary:

Verifica la validità del token fornito, restituendo dettagli sull'utente per cui questo claim è valido

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | secret response |

##### Security

| Security Schema | Scopes |
| --- | --- |
| jwt | secret |
