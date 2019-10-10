#!/usr/bin/env python3
from flask import Flask, request, render_template, redirect, send_from_directory, jsonify
import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime as dt

app = Flask(__name__, static_url_path='/ipw/static/')
app.config.from_object('config.Config')
db = SQLAlchemy(app)
# from models import Interested

class Interested(db.Model):
    __tablename__ = 'interested'
    #__table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, index=False, unique=False, nullable=False)

    def __repr__(self):
       return '<Interested {}>'.format(self.time)
from models import *
db.create_all()

@app.route('/ipw/')
def landing():
    return render_template('landing.html')

@app.route('/ipw/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/ipw/statistics')
def statistics():
    rows = Interested.query.all()
    whos = User.query.with_entities(User.who)
    # do fancy dbms stats and plots
    return render_template('stats.html', rows=rows, whos=whos)

@app.route('/ipw/interested', methods=['POST'])
def interested():
    row = Interested(time=dt.now())
    db.session.add(row)
    db.session.commit()
    return 'Success'

@app.route('/ipw/register', methods=['POST'])
def register():
    response = {'error': 0, 'message': ''}
    name = request.form['name']
    email = request.form['email']
    who = request.form['who']
    existing_user = User.query.filter(User.email == email).first()
    if existing_user:
        response['error'] = 1
        response['message'] = 'This email has already signed up'
        return jsonify(response)
    user = User(name=name, email=email,
            who=who)
    db.session.add(user)
    db.session.commit()
    return jsonify(response)

if __name__ == "__main__":
	host = "0.0.0.0"
	port = 8080
	app.run(host, port, debug=True)
