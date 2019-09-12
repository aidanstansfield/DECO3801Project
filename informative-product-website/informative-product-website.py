#!/usr/bin/env python3
from flask import Flask, request, render_template, redirect, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def landing():
    return 'landing page'

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
    
if __name__ == "__main__":
	host = "0.0.0.0"
	port = 8080
	app.run(host, port, debug=True)

