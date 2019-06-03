# Smart Home Automation

## Backend

Requirements: Python3. On Debian: `apt install python3`

```bash
cd backend
python3 -m venv .
source bin/activate
pip3 install -r requirements.txt
pip3 install connexion[swagger-ui]
python3 app.py
```

### Auth
```bash
curl -X GET "http://localhost:8080/secret" -H  "accept: text/plain" -H
 "Authorization: Bearer $TOKEN"
```

## Frontend

Requirements: Node.js and npm. 

On Debian:
```bash
curl -sL https://deb.nodesource.com/setup_12.x | bash -
apt-get install -y nodejs
```

```bash
cd frontend
npm install
npm run serve
```