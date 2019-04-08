# SHA

Marco Belotti, Francesco Bombarda, Antonio Vivace

## Getting started

```bash
# Clone the project
git clone https://github.com/avivace/sha
# Create the python virtual env (first time after cloning, only)
python3 -m venv .
# Activate the virtual env
source bin/activate
# Install requirements
pip3 install -r requirements.txt
```


Elenco Pacchetti:

```
	pip install flask
	pip install flask-wtf
	pip install flask-sqlalchemy
	pip install flask-migrate
	pip install flask-login
	pip install flask-mail
	pip install pyjwt
	pip install flask-bootstrap
	pip install flask-moment
	pip install paho-mqtt
```

Variabili ambiente:

```
	export FLASK_APP=microblog.py
	export FLASK_DEBUG=1
	export MAIL_SERVER=smtp.googlemail.com
	export MAIL_PORT=587
	export MAIL_USE_TLS=1
	export MAIL_USERNAME=<your-gmail-username>
	export MAIL_PASSWORD=<your-gmail-password>
```

Comandi DB:

```
	flask db init
	flask db migrate -m "comment"
	flask db upgrade
```	

Comandi avvio ambiente virtuale:

```
source venv/bin/activate
```
