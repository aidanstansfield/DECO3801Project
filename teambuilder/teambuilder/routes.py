#!/usr/bin/env python3
from flask import request, abort, send_from_directory, render_template, Blueprint
from flask import redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required
import os
import json
from .allocation.json_alloc import allocate
from .models import User
from flask import current_app as app

main_bp = Blueprint('main_bp', __name__, template_folder='templates',
                    static_folder='static')

# set to True when testing locally to avoid permission denied
#ignore_auth = True
"""
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
"""
# favicon route
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 
            'favicon.ico', mimetype='image/vnd.microsoft.icon')

# landing page
@main_bp.route('/')
def home():
    return render_template('landing.html')

# allocation page
@main_bp.route('/allocation')
@login_required
def allocation():
    print('in allocation')
    return render_template('allocation.html')

# courses page
@main_bp.route('/courses')
@login_required
def courses():
    return render_template('courses.html')

# course details page. Optionally takes a course ID field
@main_bp.route('/course/<id>')
@login_required
def course_info(id=None):
    return render_template('course-details.html', id=id)

"""
# logout route
@app.route('/logout')
def logout():
    return redirect('https://api.uqcloud.net/logout')
"""

# receive an allocation request from the client, and return the result of the
# allocation.
@main_bp.route('/allocator', methods=['POST'])
@login_required
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

