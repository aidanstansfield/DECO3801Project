# pip3 install Flask
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)

app.secret_key = b'7G\x07\xf9\xf8\x91\xe1\x1el\x97\xcfBH\xf1\xd2\xf9'

@app.route('/')
def basic():
    return "Hello World!"

@app.route('/basic-html')
def html():
    return render_template("basic-html.html")

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


# i know this bad login practice, just demoing session variables and other stuff
@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get("logged_in"):
        return redirect(url_for('secret'))
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        if (username == 'admin' and password == 'password'):
            session["logged_in"] = True
            return redirect(url_for('secret'))
        return render_template("login.html", error="Invalid login")
    return render_template("login.html")

@app.route('/super-secret-page')
def secret():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return "wow flask is cool"

#im lazy cba making button for logout
@app.route("/logout")
def logout():
    session['logged_in'] = False
    return redirect(url_for('login'))


# use a production WSGI server instead of the dev server packaged with Flask!
# see 
if __name__ == "__main__":
    host = "localhost"
    port = 8080
    app.run(host, port, debug=True)