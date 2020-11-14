import sys
from app import app
from flask import render_template, request, redirect, flash, url_for
import games, users
from forms import *

@app.route("/")
def index():
    print("Pääsivu latautui", file=sys.stdout)
    game_list = games.get_list()
    return render_template("index.html", games=game_list)

@app.route("/game/new", methods=["get", "post"])
def newgame():
    form = GameForm()
    if form.validate_on_submit():
        id = None
        name = request.form["name"]
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]
        price = request.form["price"]        
        location = request.form["location"]
        description = request.form["description"]
        if games.send(id, name, start_date, end_date, location, price, description):
            flash('Pelin tiedot tallennettu')
            return redirect(url_for("index"))
        else:
            flash('Pelin lisääminen ei onnistunut', 'error')
            return redirect(url_for("newgame"))
    return render_template("newgame.html", form=form, action="/game/new", title="Uuden pelin luonti")

@app.route("/game/<game_id>/edit", methods=["get", "post"])
def editgame(game_id):
    game = games.get_details(game_id)
    form = GameForm(data=game)
    if request.method == 'GET':    
        return render_template("newgame.html", form=form, action="/game/" + game_id + "/edit" , title="Pelin tietojen päivitys")
    if form.validate_on_submit():
        id = request.form["id"]
        name = request.form["name"]
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]
        location = request.form["location"]
        price = request.form["price"]
        description = request.form["description"]
        print("The id in the router is: " + str(id))
        if games.send(id, name, start_date, end_date, location, price, description):
            flash('Pelin tiedot päivitetty')
            return redirect(url_for("index"))
        else:
            flash('Pelin päivitys ei onnistunut', 'error')
            return redirect(url_for("editgame"))
    # return render_template("newgame.html", form=form)

@app.route("/game/<game_id>")
def game_details(game_id):
    game = games.get_details(game_id)
    return render_template("gamedetails.html", game=game)

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
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        nickname = request.form["nickname"]
        gender = int(request.form["gender"])
        birth_year = int(request.form["birth_year"])
        profile = request.form["profile"]    
        if users.register(email,password, first_name, last_name, nickname, gender, birth_year, profile):
            return redirect(url_for("index"))
        else:
            flash("Rekisteröinti ei onnistunut")
            return redirect(url_for("register"))
    return render_template("register.html", form=form)