#!/usr/bin/env python3
from flask import Flask, request, abort
import json

app = Flask(__name__)

@app.before_first_request
def check_auth():
    if 'staff' not in request.headers.get('X-Uq-User-Type').lower:
        abort(403)

@app.errorhandler(403)
def denied():
    # make a custom 403
    return "Permission Denied"

@app.route('/')
def home():
    return str(request.headers)

if __name__ == "__main__":
	host = "0.0.0.0"
	port = 8080
	app.run(host, port)

