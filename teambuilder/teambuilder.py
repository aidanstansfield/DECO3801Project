#!/usr/bin/env python3
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
	return "Go Away"

if __name__ == "__main__":
	host = "0.0.0.0"
	port = 8080
	app.run(host, port)

