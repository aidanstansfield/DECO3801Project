#!/usr/bin/env python3
from flask import Flask, request, abort, send_from_directory, render_template 
from flask import redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import json
from allocation.json_alloc import allocate

app = Flask(__name__)
app.config.from_object('config.Config')
# db = SQLAlchemy(app)
# from models import *
# db.create_all()

# allow these user's even if they're not staff
explicitly_allowed_users = ['s4434177', 's4200694', 's4317687', 's4386414', 
    's4432329', 's4436755'] 

# set to True when testing locally to avoid permission denied
ignore_auth = True

# Before every request, run this function.
# This will return a 403 permission denied if the user is trying to access 
# content they're not allowed to.
@app.before_request
def check_auth():
    if ignore_auth or \
        request.path == '/' or request.path.startswith('/static/') \
        or (
            request.headers.get('X-Uq-User-Type') != None and
            'staff' in request.headers.get('X-Uq-User-Type').lower()
        ) or (
            request.headers.get('X-Uq-User') != None and
            request.headers.get('X-Uq-User').lower() in explicitly_allowed_users
        ):
        return
    # if we haven't returned, user is not allowed
    abort(403)

# Handle the 403 error ourselves
@app.errorhandler(403)
def denied(e):
    # make a custom 403 html file
    return "Permission Denied", 403

# favicon route
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 
            'favicon.ico', mimetype='image/vnd.microsoft.icon')

# landing page
@app.route('/')
def home():
    return render_template('landing.html')

# allocation page
@app.route('/allocation')
def allocation():
    return render_template('allocation.html')

# courses page
@app.route('/courses')
def courses():
    return render_template('courses.html')

# course details page. Optionally takes a course ID field
@app.route('/course/<id>')
def course_info(id=None):
    return render_template('course-details.html', id=id)

# logout route
@app.route('/logout')
def logout():
    return redirect('https://api.uqcloud.net/logout')

# receive an allocation request from the client, and return the result of the
# allocation.
@app.route('/allocator', methods=['POST'])
def allocator():
    print(request.json)
    response = app.response_class(
        response = allocate(json.dumps(request.json)),
        status = 200,
        mimetype = 'application/json'
    )
    return response 

# this will only run if we're running the script manually (i.e. debugging)
if __name__ == "__main__":
	host = "0.0.0.0"
	port = 8080
	app.run(host, port, debug=True)

