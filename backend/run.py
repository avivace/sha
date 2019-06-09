#!/usr/bin/env python3

from app import initConnexApp

app = initConnexApp()
app.run(debug=True,use_reloader=True,port=8081)