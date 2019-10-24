#!/usr/bin/env python3
from flask import request, abort, send_from_directory, render_template, Blueprint
from flask import redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, current_user
import os
import json
from .allocation.json_alloc import allocate
from .models import User, Course, Student
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

@main_bp.route('/course/<int:id>/allocate')
@login_required
def course_allocation(id=id):
    return render_template('allocation.html')

# courses page
@main_bp.route('/courses')
@login_required
def courses():
    courses = []
    for course in current_user.courses:
        num_students = len(course.students)
        num_responded = sum(1 for student in course.students 
                if student.response != None and student.response != '')
        courses.append({'cid': course.cid, 'name': course.name, 
                'num_responded': num_responded, 'num_pending': num_students - 
                num_responded})
    return render_template('courses.html', courses=courses)

# course details page. Optionally takes a course ID field
@main_bp.route('/course/<id>')
@login_required
def course_info(id=None):
    return render_template('course-details.html', id=id)

# receive an allocation request from the client, and return the result of the
# allocation.
@main_bp.route('/allocate', methods=['POST'])
@login_required
def run_allocation():
    response = app.response_class(
        response = allocate(json.dumps(request.json)),
        status = 200,
        mimetype = 'application/json'
    )
    return response 

@main_bp.route('/survey/<int:id>')
def survey(id=None):
    if (id == None):
        return "The URL you have input is complete" # maybe make this pretty
    username = request.headers.get('X-Uq-User')
    if username == None:
        # there was no X-Uq-User.
        username = 's4434177' # testing, remove later
        # return "There was an error retrieving your username from UQ SSO."
    course = Course.query.filter_by(cid=id).first()
    if (course == None):
        return "The URL you have input is invalid"
    student = Student.query.filter_by(cid=id, sid=username).first()
    if (student == None):
        return "You are not a part of the course this survey regards."
    return "put template for survey here"

"""
# Example how to create course & student
new_course = Course(name='putnamehere', questions='putquestionshere', 
        uid=current_user.id)
db.session.add(new_course)
new_student = Student(sid='puttheiridhere',cid=new_course.cid,
        name='putnamehere, or dont, name is optional for anon', 
        response='you can leave this out since it wont be set till they respond')
db.session.add(new_student)
# and finally
db.session.commit()
"""

# this will only run if we're running the script manually (i.e. debugging)
if __name__ == "__main__":
	host = "0.0.0.0"
	port = 8080
	app.run(host, port, debug=True)

