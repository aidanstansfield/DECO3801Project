#!/usr/bin/env python3
from flask import Flask, request, abort, send_from_directory, render_template, make_response, redirect
import os

app = Flask(__name__)

explicitly_allowed_users = ['s4434177', 's4200694', 's4317687', 's4386414', 
    's4432329', 's4436755']
ignore_auth = False

@app.before_request
def check_auth():
    if ignore_auth or request.path == '/' or request.path.startswith('/static/') or \
	    (request.headers.get('X-Uq-User-Type') != None and \
            'staff' in request.headers.get('X-Uq-User-Type').lower()) or \
            (request.headers.get('X-Uq-User') != None and \
            request.headers.get('X-Uq-User').lower() in explicitly_allowed_users):
        return
    # if we haven't returned, user is not allowed
    abort(403)

@app.errorhandler(403)
def denied(e):
    # make a custom 403 html file
    return "Permission Denied", 403

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
def home():
    #return str(request.headers)
    return render_template('landing.html')

@app.route('/allocation')
def allocation():
    return render_template('allocation.html')

@app.route('/logout')
def logout():
    return redirect('https://api.uqcloud.net/logout')

if __name__ == "__main__":
	host = "0.0.0.0"
	port = 8080
	app.run(host, port, debug=True)

