import sys
from app import app
from flask import render_template, request, redirect, flash, url_for
import games, users, gameforms
from forms import *

@app.route("/")
def index():
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
    return render_template("game_editor.html", form=form, action="/game/new", title="Uuden pelin luonti", has_form=False, his_published=False)

@app.route("/game/<game_id>/edit", methods=["get", "post"])
def editgame(game_id):
    game = games.get_details(game_id)
    if users.user_id() not in map(lambda org: org['id'], game['organisers']):
        return redirect(url_for("index"))
    form = GameForm(data=game)
    if request.method == 'GET':
        has_form = False if gameforms.get_game_form(game_id) is None else True
        is_published = gameforms.is_published(game_id)
        return render_template("game_editor.html", form=form, action="/game/" + game_id + "/edit" , title=game['name'] + ": Tietojen päivitys", has_form=has_form, is_published=is_published)
    if form.validate_on_submit():
        name = request.form["name"]
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]
        location = request.form["location"]
        price = request.form["price"]
        description = request.form["description"]
        if games.send(game_id, name, start_date, end_date, location, price, description):
            if form.create_form.data:
                game_form = gameforms.create_game_form(game_id)
                gameforms.insert_default_questions(game_form['id'])
                return redirect("/game/" + game_id + "/form/edit")
            elif form.edit_form.data:
                return redirect("/game/" + game_id + "/form/edit")    
            else:
                flash('Pelin tiedot päivitetty')
                return redirect(url_for("index"))
        else:
            flash('Pelin päivitys ei onnistunut', 'error')
            return redirect(url_for("editgame"))

@app.route("/game/<game_id>")
def game_details(game_id):
    game = games.get_details(game_id)
    return render_template("gamedetails.html", game=game)

# For now, game organisers can only create a default form, view it and publish it. 
# The form editing functionality will be added in the next phase of the project.
@app.route("/game/<game_id>/form/edit", methods=["get", "post"])
def editform(game_id):
    game = games.get_details(game_id)
    if users.user_id() not in map(lambda org: org['id'], game['organisers']):
        return redirect(url_for("index"))
    if request.method == 'GET':
        gameform = gameforms.get_game_form(game_id)
        form_data = {"form_id": gameform['id'], "form_name": gameform['name'], "published": gameform['published']}
        form = RegistrationForm(data=form_data)
        questions = gameforms.get_default_questions() if gameforms.get_form_questions(gameform['id']) is None else gameforms.get_form_questions(gameform['id'])        
        for question in questions:
            question['options'] = gameforms.get_question_options(question['id'])
        return render_template("form_editor.html", game=game, form=form, questions=questions, action="/game/" + game_id + "/form/publish" , title="Ilmoittautumislomakkeen muokkaus: " + game['name'])

@app.route("/game/<game_id>/form/publish", methods=["post"])
def publishform(game_id):
    print(request.form['form_id'])
    if 'publish' in request.form:
        gameforms.publish_form(request.form['form_id'])
    if 'cancel' in request.form:
        gameforms.cancel_form(request.form['form_id'])
    return redirect("/game/" + str(game_id) + "/edit")

@app.route("/game/<game_id>/register", methods=["get", "post"])
def gameregistration(game_id):
    game = games.get_details(game_id)
    gameform = gameforms.get_game_form(game_id)
    form_data = {"form_id": gameform['id'], "form_name": gameform['name'], "published": gameform['published']}
    form = RegistrationForm(data=form_data)
    if request.method == 'GET':    
        questions = gameforms.get_form_questions(gameform['id'])        
        for question in questions:
            question['options'] = gameforms.get_question_options(question['id'])
        return render_template("registration.html", game=game, form=form, questions=questions, action="/game/" + game_id + "/register" , title="Ilmoittautuminen: " + game['name'])
    if form.validate_on_submit():
        answer_list = []
        for key, value in request.form.items():
            if "checkbox" in key or "radio" in key:
                answer_list.append({"person_id": users.user_id(), "formquestion_id": key.split("_")[1], "questionoption_id": value})
            elif "integer" in key or "string" in key or "textarea" in key:
                answer_list.append({"person_id": users.user_id(), "formquestion_id": key.split("_")[1], "answer_text": value})
        if gameforms.save_answers(answer_list):
            flash('Ilmoittautuminen tallennettu')
            return redirect(url_for("index"))
        else:
            flash('Ilmoittautuminen ei onnistunut', 'error')
            return redirect("/game/" + game_id + "/register")

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