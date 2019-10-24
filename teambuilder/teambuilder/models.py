from . import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    """Model for user accounts."""

    __tablename__ = 'users'

    # NOTE; must be called 'id' for UserMixin goodness
    id = db.Column(db.Integer, primary_key=True) 
    username = db.Column(db.String, nullable=False, unique=True)
    courses = db.relationship('Course', backref='users', lazy=True)

class Course(db.Model):
    __tablename__ = 'courses'

    cid = db.Column(db.Integer, primary_key=True)
    # if you don't want courses with same name (per user), do some validation 
    # upon creation
    name = db.Column(db.String, nullable=False)
    # a json dump of the questions
    questions = db.Column(db.Text, nullable=True)
    uid = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    students = db.relationship('Student', backref='courses', lazy=True)

class Student(db.Model):
    __tablename__ = 'students'

    sid = db.Column(db.String, primary_key=True, nullable=False)
    cid = db.Column(db.Integer, db.ForeignKey('courses.cid'), primary_key=True)
    sname = db.Column(db.String, nullable=True) # allow for anon users
    # a json dump of the survey response
    response = db.Column(db.Text, nullable=True) 