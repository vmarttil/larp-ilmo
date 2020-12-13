import sys
from app import app
from flask import render_template, request, redirect, flash, url_for, session
import datetime
import games, users, gameforms
from forms import *

@app.route("/game/new", methods=["get", "post"])
def newgame():
    '''Display the new game creation form on GET and save the new game on POST.'''
    form = GameForm(meta={'locales': ['fi_FI', 'fi']})
    if form.validate_on_submit():
        if users.user_id() > 0:
            game_id = None
            name = request.form["name"]
            start_date = datetime.datetime.strptime(request.form["start_date"], '%d.%m.%Y')
            end_date = datetime.datetime.strptime(request.form["end_date"], '%d.%m.%Y')
            price = request.form["price"]        
            location = request.form["location"]
            description = request.form["description"]
            if games.send(users.user_id(), game_id, name, start_date, end_date, location, price, description):
                flash("Pelin tiedot tallennettu", "success")
                return redirect(url_for("index"))
            else:
                flash("Pelin lisääminen ei onnistunut", "error")
                return redirect(url_for("newgame"))
    return render_template("game_editor.html", form=form, action="/game/new", title="Uuden pelin luonti", has_form=False, his_published=False)

@app.route("/game/<game_id>/edit", methods=["get", "post"])
def editgame(game_id):
    '''Display the game editor form on GET and save the edited game on POST.'''
    game = games.get_details(game_id)
    game['start_date'] = game['start_date'].strftime('%d.%m.%Y')
    game['end_date'] = game['end_date'].strftime('%d.%m.%Y')
    if users.user_id() not in map(lambda org: org['id'], game['organisers']):
        return redirect(url_for("index"))
    form = GameForm(data=game, meta={'locales': ['fi_FI', 'fi']})
    if request.method == 'GET':
        has_form = False if gameforms.get_game_form(game_id) is None else True
        is_published = gameforms.is_published(game_id)
        return render_template("game_editor.html", form=form, action="/game/" + game_id + "/edit" , title=game['name'] + ": Tietojen päivitys", has_form=has_form, is_published=is_published)
    if request.method == 'POST':
        if 'create_form' in request.form:
            game_form = gameforms.create_game_form(game_id)
            gameforms.insert_default_questions(game_form['id'])
            return redirect("/game/" + game_id + "/form/edit")
        elif 'edit_form' in request.form:
            return redirect("/game/" + game_id + "/form/edit")
        elif 'publish_form' in request.form:
            gameforms.publish_form(gameforms.get_game_form(game_id)["id"])
            flash("Pelin ilmoittautuminen avattu", "success")
            return redirect("/game/" + game_id + "/edit")
        elif 'unpublish_form' in request.form:
            gameforms.unpublish_form(gameforms.get_game_form(game_id)["id"])
            flash("Pelin ilmoittautuminen suljettu", "success")
            return redirect("/game/" + game_id + "/edit")
    if form.validate_on_submit():
        name = request.form["name"]
        start_date = datetime.datetime.strptime(request.form["start_date"], '%d.%m.%Y')
        end_date = datetime.datetime.strptime(request.form["end_date"], '%d.%m.%Y')
        location = request.form["location"]
        price = request.form["price"]
        description = request.form["description"]
        if games.send(users.user_id(), game_id, name, start_date, end_date, location, price, description):
            flash("Pelin tiedot päivitetty", "success")
            return redirect("/game/" + game_id + "/edit")
        else:
            flash("Pelin tietojen päivitys ei onnistunut", "error")
            return redirect("/game/" + game_id + "/edit")

@app.route("/game/<game_id>")
def game_details(game_id):
    '''Display the details of the given game.'''
    game = games.get_details(game_id)
    if users.user_id() in map(lambda org: org['id'], game['organisers']):
        registrations = games.get_registrations(game_id)
        return render_template("gamedetails.html", game=game, organiser=True, registrations=registrations)
    else:
        return render_template("gamedetails.html", game=game, organiser=False)

@app.route("/game/<game_id>/register", methods=["get", "post"])
def gameregistration(game_id):
    '''Display the game registration form for the given game on GET and save the registration on POST.'''
    game = games.get_details(game_id)
    gameform = gameforms.get_game_form(game_id)
    form_data = {"form_id": gameform['id'], "form_name": gameform['name'], "published": gameform['published']}
    if gameform['published'] == False:
        return redirect(url_for("index"))
    form = RegistrationForm(data=form_data, meta={'locales': ['fi_FI', 'fi']})
    if request.method == 'GET':    
        question_list = gameforms.get_form_questions(gameform['id'])
        prefill_data = users.get_prefill_data(game)
        for question in question_list:
            question['options'] = questions.get_question_options(question['id'])
        return render_template("registration.html", game=game, form=form, question_list=question_list, prefill_data=prefill_data, action="/game/" + game_id + "/register" , title="Ilmoittautuminen: " + game['name'], mode="register")
    if form.validate_on_submit():
        answer_list = []
        for key, value in request.form.items():
            if "checkbox" in key or "radio" in key:
                answer_list.append({"person_id": users.user_id(), "formquestion_id": key.split("_")[1], "option_id": value})
            elif "integer" in key or "string" in key or "textarea" in key:
                answer_list.append({"person_id": users.user_id(), "formquestion_id": key.split("_")[1], "answer_text": value})
        if answers.save_answers(users.user_id(), game_id, answer_list):
            flash("Ilmoittautuminen tallennettu", "success")
            return redirect(url_for("index"))
        else:
            flash("Ilmoittautuminen ei onnistunut", "error")
            return redirect("/game/" + game_id + "/register")

@app.route("/game/<game_id>/registration/<registration_id>", methods=["get"])
def viewgameregistration(game_id, registration_id):
    '''Display the given registration for the given game.'''
    game = games.get_details(game_id)
    if users.user_id() not in map(lambda org: org['id'], game['organisers']):
        return redirect(url_for("index"))
    gameform = gameforms.get_game_form(game_id)
    form_data = {"form_id": gameform['id'], "form_name": gameform['name'], "published": gameform['published']}
    form = RegistrationForm(data=form_data, meta={'locales': ['fi_FI', 'fi']})
    question_list = gameforms.get_form_questions(gameform['id'])        
    for question in question_list:
        question['options'] = questions.get_question_options(question['id'])
        question['answer'] = answers.get_question_answer(registration_id, question['id'])
    return render_template("registration.html", form=form, question_list=question_list, action="", title="Ilmoittautuminen: " + game['name'], mode="game", game_id=game_id)