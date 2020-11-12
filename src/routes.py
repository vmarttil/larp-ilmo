import sys
from app import app
from flask import render_template, request, redirect, flash, url_for
import games, users
from forms import *

@app.route("/")
def index():
    print("Pääsivu latautui", file=sys.stdout)
    list = games.get_list()
    return render_template("index.html", games=list)

@app.route("/newgame", methods=["get", "post"])
def newgame():
    form = GameForm()
    if form.validate_on_submit():
        name = request.form["name"]
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]
        location = request.form["location"]
        description = request.form["description"]
        if games.send(name, start_date, end_date, location, description):
            flash('Pelin tiedot tallennettu')
            return redirect(url_for("index"))
        else:
            flash('Pelin lisääminen ei onnistunut', 'error')
            return redirect(url_for("newgame"))
    return render_template("newgame.html", form=form)

@app.route("/login", methods=["get","post"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = request.form["email"]
        password = request.form["password"]
        if users.login(email,password):
            return redirect(url_for("index"))
        else:
            flash('Väärä sähköpostiosoite tai salasana')
            return redirect(url_for("login"))
    return render_template('login.html', form=form)

@app.route("/logout")
def logout():
    users.logout()
    return redirect(url_for("index"))

@app.route("/register", methods=["get","post"])
def register():
    print("Rekisteröintilomake latautui")
    form = RegisterForm()
    if form.validate_on_submit():
        print("Rekisteröintilomake lähti")
        email = request.form["email"]
        password = request.form["password"]
        name = request.form["name"]
        gender = int(request.form["gender"])
        birth_year = int(request.form["birth_year"])
        profile = request.form["profile"]    
        if users.register(email,password, name, gender, birth_year, profile):
            return redirect(url_for("index"))
        else:
            flash("Rekisteröinti ei onnistunut")
            return redirect(url_for("register"))
    return render_template("register.html", form=form)