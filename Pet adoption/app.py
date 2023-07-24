from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import json

app = Flask(__name__)


def connect_db():
    c = sqlite3.connect("pet registration.db").cursor()
    c.execute("CREATE TABLE IF NOT EXISTS Pet("
              "Name TEXT, Category TEXT, Age INTEGER, Weight INTEGER, Rescue_background TEXT)"
              )
    c.connection.close()


database = {"Erfan": "Erfan123", "John": "John123"}


@app.route('/', methods=['GET'])
def home_page():
    connect_db()
    data = getpets()
    return render_template("login.html")


@app.route('/getpets', methods=['GET'])
def getpets():
    c = sqlite3.connect("pet registration.db").cursor()
    c.execute("SELECT * FROM pet registration")
    data = c.fetchall
    return data


@app.route('/success/<name>/<password>')
def Success(name, passwrd):
    if name in database.keys():
        if passwrd == database[name]:
            return "<h1>Welcome to Pet Adoption Centre</h1>"
        else:
            return "<h1>Invalid Username of Password.</h1>"
    else:
        return "<h1>Username doesn't exist.</h1>"


@app.route('/fetch_data', methods=['POST', 'GET'])
def FetchData():
    if request.method == 'POST':
        user = request.form['nm']
        password = request.form['pw']
        return redirect(url_for('Success', name=user, passwrd=password))
    else:
        user = request.args.get('nm')
        password = request.args.get('pw')
        return redirect(url_for('Success', name=user, passwrd=password))


@app.route('/signup_page')
def signup_page():
    return render_template("signup.html")


@app.route('/registered/<name>/<password>/<cnfpass>')
def Registered(name, passwrd, cnfpass):
    if passwrd == cnfpass:
        database.update({name: passwrd})
        return "<h1>Successfully signed Up.</h1>"
    else:
        return "<h1>Password didnot match</h1>"


@app.route('/signup', methods=['POST', 'GET'])
def Signup():
    if request.method == "POST":
        user = request.form['snm']
        password = request.form['spw']
        cpassword = request.form['scpw']
        return redirect(url_for('Registered', name=user, passwrd=password, cnfpass=cpassword))
    else:
        user = request.args.get('snm')
        password = request.args.get('spw')
        cpassword = request.args.get('scpw')
        return redirect(url_for('Registered', cnfpass=cpassword, name=user, passwrd=password))


if __name__ == "__main__":
    app.run(debug=True)


