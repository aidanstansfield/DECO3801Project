#!/usr/bin/env python3
from flask import request, abort, send_from_directory, render_template, Blueprint, url_for
from flask import redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, current_user
import os
import json
from .allocation.json_alloc import allocate
from .models import User, Course, Student
from flask import current_app as app
from . import db

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

# allocation page. TO BE DELETED & REPLACED WITH BELOW
@main_bp.route('/allocation')
@login_required
def allocation():
    return render_template('allocation.html', page_title='Title Here', require_back_btn=True, 
        back_btn_link='/courses', back_btn_text='All Courses', questions = 'foo')

@main_bp.route('/course/<int:id>/allocate')
@login_required
def course_allocation(id=id):
    course = Course.query.filter_by(cid=id).first()
    if course == None:
        return "didn't find it"
    return render_template('allocation.html', page_title=course.name, 
        require_back_btn=True, back_btn_link='/courses', back_btn_text='All Courses',
        questions=course.questions, cid=id)

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
                num_responded, 'survey_url': request.url_root + url_for('main_bp.survey', id=course.cid)[1:]})
    return render_template('courses.html', courses=courses, page_title='My Courses')

# course creation page
@main_bp.route('/create-course')
@login_required
def create_course():
    return render_template('create-course.html', page_title='Create New Course', require_back_btn=True, back_btn_link='/courses', back_btn_text='All Courses')

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
    data = request.json
    cid = data.get('cid')
    course = Course.query.filter_by(cid=cid).first()
    if (course == None):
        return "Could not find that course"
    students = {}
    for student in course.students:
        if student.response != None and student.response != '':
            students[student.sid] = json.loads(student.response)
    data.pop('cid')
    data['students'] = students
    response = app.response_class(
        response = allocate(json.dumps(data)),
        status = 200,
        mimetype = 'application/json'
    )
    return response 

@main_bp.route('/survey/<int:id>', methods=['GET', 'POST'])
def survey(id=None):
    if (id == None):
        return "The URL you have input is complete" # maybe make this pretty
    username = request.headers.get('X-Uq-User')
    if username == None:
        # there was no X-Uq-User.
        if (app.config['FLASK_ENV'] == 'development'):
            username = 's4434177' # testing, remove later
        else:
            return "There was an error retrieving your username from UQ SSO."
    course = Course.query.filter_by(cid=id).first()
    if (course == None):
        return "The URL you have input is invalid"
    student = Student.query.filter_by(cid=id, sid=username).first()
    if (student == None):
        return "You are not a part of the course this survey regards."
    if request.method == 'GET':
        return "put template for survey here"#render_template('survey.html', questions=course.questions)
    else:
        response = request.json
        student.response = json.dumps(response)
        db.session.commit()

""" Danie put this into course create
# To go into the create_course page:
if request.method == 'GET':
    return render_template('create_course.html')
# otherwise it's post, assuming you've set methods=['GET', 'POST'] in route
data = request.json
# Create course & student
new_course = Course(name=data.get('name'), questions=json.dumps(data.get('questions')), 
        uid=current_user.id)
db.session.add(new_course)
for student in data.get('students'):
    new_student = Student(sid=student.get('sid'), cid=new_course.cid,
        name=student.get('name'))
    db.session.add(new_student)
# and finally
db.session.commit()
"""


# this will only run if we're running the script manually (i.e. debugging)
if __name__ == "__main__":
	host = "0.0.0.0"
	port = 8080
	app.run(host, port, debug=True)

