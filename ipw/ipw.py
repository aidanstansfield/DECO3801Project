#!/usr/bin/env python3
from flask import Flask, request, render_template, redirect, send_from_directory
import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime as dt

app = Flask(__name__, static_url_path='/ipw/static/')
#app.config.from_object('config.Config')

app.config['SECRET_KEY'] = '\xb7)\xa8\x9d\xd3\xa1\xeaG[+\xe3\xfa\xe0\xb2\xe2j'
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://allotech:allotech@localhost/ipw'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#db = SQLAlchemy(app)
#from models import Interested

#class Interested(db.Model):
#    __tablename__ = 'interested'
#    #__table_args__ = {'extend_existing': True}
#    id = db.Column(db.Integer, primary_key=True)
#    time = db.Column(db.DateTime, index=False, unique=False, nullable=False)
#
#    def __repr__(self):
#        return '<Interested {}>'.format(self.time)
#db.create_all()

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
    # do fancy dbms stats and plots
    return render_template('stats.html', rows=rows)

@app.route('/ipw/interested', methods=['POST'])
def interested():
    #row = Interested(time=dt.now())
    #db.session.add(row)
    #db.session.commit()
    return 'Change this to be asynchronous js'

if __name__ == "__main__":
	host = "0.0.0.0"
	port = 8080
	app.run(host, port, debug=True)
