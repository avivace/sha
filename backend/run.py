#!/usr/bin/env python3

# Main software entrypoint
from app import initConnexApp

# Initialise and start the configured Connexion app
app = initConnexApp()

app.run(debug=True, use_reloader=True, port=8081)