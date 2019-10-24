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
    return render_template('allocation.html', page_title='Title Here', require_back_btn=True, back_btn_link='/courses', back_btn_text='All Courses')

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

# receive an allocation request from the client, and return the result of the
# allocation.
@main_bp.route('/allocator', methods=['POST'])
@login_required
def allocator():
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

