import sys
from app import app
from flask import render_template, request, redirect, flash, url_for, session
import datetime
import games, users, gameforms
from forms import *

@app.route("/")
def index():
    game_list = games.get_list()
    return render_template("index.html", games=game_list)

@app.route("/game/new", methods=["get", "post"])
def newgame():
    form = GameForm(meta={'locales': ['fi_FI', 'fi']})
    if form.validate_on_submit():
        id = None
        name = request.form["name"]
        start_date = datetime.datetime.strptime(request.form["start_date"], '%d.%m.%Y')
        end_date = datetime.datetime.strptime(request.form["end_date"], '%d.%m.%Y')
        price = request.form["price"]        
        location = request.form["location"]
        description = request.form["description"]
        if games.send(id, name, start_date, end_date, location, price, description):
            flash("Pelin tiedot tallennettu", "success")
            return redirect(url_for("index"))
        else:
            flash("Pelin lisääminen ei onnistunut", "error")
            return redirect(url_for("newgame"))
    return render_template("game_editor.html", form=form, action="/game/new", title="Uuden pelin luonti", has_form=False, his_published=False)

@app.route("/game/<game_id>/edit", methods=["get", "post"])
def editgame(game_id):
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
            gameforms.publish_form(request.form['form_id'])
            return redirect(/game/" + game_id + "/edit)
        elif 'unpublish_form' in request.form:
            gameforms.unpublish_form(request.form['form_id'])
            return redirect(/game/" + game_id + "/edit)
    if form.validate_on_submit():
        name = request.form["name"]
        start_date = datetime.datetime.strptime(request.form["start_date"], '%d.%m.%Y')
        end_date = datetime.datetime.strptime(request.form["end_date"], '%d.%m.%Y')
        location = request.form["location"]
        price = request.form["price"]
        description = request.form["description"]
        if games.send(game_id, name, start_date, end_date, location, price, description):
            flash("Pelin tiedot päivitetty", "success")
            return redirect(/game/" + game_id + "/edit)
        else:
            flash("Pelin tietojen päivitys ei onnistunut", "error")
            return redirect(/game/" + game_id + "/edit)

@app.route("/game/<game_id>")
def game_details(game_id):
    game = games.get_details(game_id)
    if users.user_id() in map(lambda org: org['id'], game['organisers']):
        registrations = games.get_registrations(game_id)
        return render_template("gamedetails.html", game=game, organiser=True, registrations=registrations)
    else:
        return render_template("gamedetails.html", game=game, organiser=False)

@app.route("/game/<game_id>/form/edit", methods=["get", "post"])
def editform(game_id):
    game = games.get_details(game_id)
    if users.user_id() not in map(lambda org: org['id'], game['organisers']):
        return redirect(url_for("index"))
    gameform = gameforms.get_game_form(game_id)
    form_data = {"form_id": gameform['id'], "form_name": gameform['name']}
    form = FormEditForm(data=form_data, meta={'locales': ['fi_FI', 'fi']})
    field_types = gameforms.get_field_types()
    if request.method == 'GET':
        questions = gameforms.get_form_questions(gameform['id'])        
        for question in questions:
            question['options'] = gameforms.get_question_options(int(question['id']))
        return render_template("form_editor.html", game=game, form=form, questions=questions, field_types=field_types, action="/game/" + game_id + "/form/edit", title="Ilmoittautumislomakkeen muokkaus")    
    elif form.validate_on_submit() and request.form.get('field_type'):
        form_data = {"form_id": request.form['form_id'], "field_type": request.form['field_type'], "option_ids": ""}
        field_type = (request.form['field_type'])
        field_type_name = gameforms.get_field_type_name(request.form['field_type'])
        form = NewQuestionForm(data=form_data, meta={'locales': ['fi_FI', 'fi']})
        return render_template("new_question.html", form=form, game=game, field_type=field_type, options=[], action="/game/" + game_id + "/form/edit/new_question", title="Uuden kysymyksen luonti: " + field_type_name)
    else:
        return redirect("/game/" + game_id + "/form/edit")

@app.route("/game/<game_id>/form/edit/move_up", methods=["post"])
def editform_move_up(game_id):
    form_id = request.form["form_id"]
    current_pos = request.form["move_up"]
    gameforms.move_question_up(form_id, current_pos)
    return redirect("/game/" + game_id + "/form/edit")

@app.route("/game/<game_id>/form/edit/move_down", methods=["post"])
def editform_move_down(game_id):
    form_id = request.form["form_id"]
    current_pos = request.form["move_down"]
    gameforms.move_question_down(form_id, current_pos)
    return redirect("/game/" + game_id + "/form/edit")

@app.route("/game/<game_id>/form/edit/edit", methods=["post"])
def editform_edit(game_id):
    return "Kysymysten muokkausta ei ole vielä toteutettu, vaan se toteutetaan projektin viimeistelyvaiheessa."

@app.route("/game/<game_id>/form/edit/delete", methods=["post"])
def editform_delete(game_id):
    return "Kysymysten poistoa ei ole vielä toteutettu, vaan se toteutetaan projektin viimeistelyvaiheessa."

@app.route("/game/<game_id>/form/edit/new_question", methods=["post"])
def editform_new_question(game_id):
    form_id = request.form["form_id"]
    field_type = request.form["field_type"]
    question_text = request.form["text"]
    description = request.form["description"]
    if gameforms.add_new_question(form_id, field_type, question_text, description):
        flash("Kysymys lisätty", "success")
        return redirect("/game/" + game_id + "/form/edit")
    else:
        flash("Kysymyksen lisääminen ei onnistunut", "error")
        return redirect("/game/" + game_id + "/form/edit")

# @app.route("/game/<game_id>/form/edit/new_option", methods=["post"])
# def editform_new_option(game_id):
#     game = games.get_details(game_id)
#     option_ids = request.form["option_ids"]
#     if request.form["option_text"] != "":
#         option_text = request.form["option_text"]
#         option_id = gameforms.add_new_option(option_text)
#         option_ids = str(option_id) if option_ids == "" else option_ids + "," + str(option_id)
#     if option_ids == "":
#         options = []
#     else:
#         options = gameforms.get_option_texts(option_ids)
#     print("Option_ids: " + option_ids)
#     form_data = {"option_ids": 3 ,"form_id": request.form['form_id'], "field_type": request.form['field_type']}
#     form = NewQuestionForm(data=form_data, meta={'locales': ['fi_FI', 'fi']})
#     form.option_ids.value = option_ids
#     field_type = request.form['field_type']
#     field_type_name = gameforms.get_field_type_name(request.form['field_type'])
#     return render_template("new_question.html", form=form, game=game, field_type=field_type, options=options, action="/game/" + game_id + "/form/edit/new", title="Uuden kysymyksen luonti: " + field_type_name)

@app.route("/game/<game_id>/form/preview", methods=["get"])
def previewform(game_id):
    game = games.get_details(game_id)
    if users.user_id() not in map(lambda org: org['id'], game['organisers']):
        return redirect(url_for("index"))
    gameform = gameforms.get_game_form(game_id)
    form_data = {"form_id": gameform['id'], "form_name": gameform['name']}
    form = RegistrationForm(data=form_data, meta={'locales': ['fi_FI', 'fi']})
    questions = gameforms.get_form_questions(gameform['id'])        
    for question in questions:
        question['options'] = gameforms.get_question_options(int(question['id']))
    return render_template("form_preview.html", game=game, form=form, questions=questions, action="" , title="Ilmoittautumislomakkeen esikatselu")

@app.route("/game/<game_id>/register", methods=["get", "post"])
def gameregistration(game_id):
    game = games.get_details(game_id)
    gameform = gameforms.get_game_form(game_id)
    form_data = {"form_id": gameform['id'], "form_name": gameform['name'], "published": gameform['published']}
    form = RegistrationForm(data=form_data, meta={'locales': ['fi_FI', 'fi']})
    if request.method == 'GET':    
        questions = gameforms.get_form_questions(gameform['id'])
        prefill_data = users.get_prefill_data(game)
        for question in questions:
            question['options'] = gameforms.get_question_options(question['id'])
        return render_template("registration.html", game=game, form=form, questions=questions, prefill_data=prefill_data, action="/game/" + game_id + "/register" , title="Ilmoittautuminen: " + game['name'], mode="register")
    if form.validate_on_submit():
        answer_list = []
        for key, value in request.form.items():
            if "checkbox" in key or "radio" in key:
                answer_list.append({"person_id": users.user_id(), "formquestion_id": key.split("_")[1], "questionoption_id": value})
            elif "integer" in key or "string" in key or "textarea" in key:
                answer_list.append({"person_id": users.user_id(), "formquestion_id": key.split("_")[1], "answer_text": value})
        if gameforms.save_answers(users.user_id(), game_id, answer_list):
            flash("Ilmoittautuminen tallennettu", "success")
            return redirect(url_for("index"))
        else:
            flash("Ilmoittautuminen ei onnistunut", "error")
            return redirect("/game/" + game_id + "/register")

@app.route("/game/<game_id>/registration/<registration_id>", methods=["get"])
def viewgameregistration(game_id, registration_id):
    game = games.get_details(game_id)
    if users.user_id() not in map(lambda org: org['id'], game['organisers']):
        return redirect(url_for("index"))
    gameform = gameforms.get_game_form(game_id)
    form_data = {"form_id": gameform['id'], "form_name": gameform['name'], "published": gameform['published']}
    form = RegistrationForm(data=form_data, meta={'locales': ['fi_FI', 'fi']})
    questions = gameforms.get_form_questions(gameform['id'])        
    for question in questions:
        question['options'] = gameforms.get_question_options(question['id'])
        question['answer'] = gameforms.get_question_answer(registration_id, question['id'], gameform['id'])
    return render_template("registration.html", form=form, questions=questions, action="", title="Ilmoittautuminen: " + game['name'], mode="game", game_id=game_id)

@app.route("/user/profile", methods=["get", "post"])
def editprofile():
    profile = users.get_profile()
    profile['birth_date'] = profile['birth_date'].strftime('%d.%m.%Y')
    form = ProfileForm(data=profile, meta={'locales': ['fi_FI', 'fi']})
    if form.validate_on_submit():
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        nickname = request.form["nickname"]
        gender = int(request.form["gender"])
        birth_date = datetime.datetime.strptime(request.form["birth_date"], '%d.%m.%Y')
        profile = request.form["profile"]    
        if users.update(first_name, last_name, nickname, gender, birth_date, profile):
            flash("Käyttäjäprofiili päivitetty", "success")
            return redirect(url_for("editprofile"))
        else:
            flash("Käyttäjäprofiilin päivitys ei onnistunut", "error")
            return redirect(url_for("editprofile"))
    registrations = users.get_registrations()
    return render_template("profile.html", form=form, email=profile['email'], registrations=registrations, title=session.get("user_name","") + ": Käyttäjäprofiili")

@app.route("/user/profile/registration/<registration_id>", methods=["get"])
def viewpersonregistration(registration_id):
    user_profile = users.get_profile()
    game_id = games.get_registration_game(registration_id)
    game = games.get_details(game_id)
    gameform = gameforms.get_game_form(game_id)
    form_data = {"form_id": gameform['id'], "form_name": gameform['name'], "published": gameform['published']}
    form = RegistrationForm(data=form_data, meta={'locales': ['fi_FI', 'fi']})
    questions = gameforms.get_form_questions(gameform['id'])        
    for question in questions:
        question['options'] = gameforms.get_question_options(question['id'])
        question['answer'] = gameforms.get_question_answer(registration_id, question['id'], gameform['id'])
    return render_template("registration.html", form=form, questions=questions, action="", title="Ilmoittautuminen: " + game['name'], mode="person")

@app.route("/login", methods=["get","post"])
def login():
    form = LoginForm(meta={'locales': ['fi_FI', 'fi']})
    if form.validate_on_submit():
        email = request.form["email"]
        password = request.form["password"]
        if users.login(email,password):
            return redirect(url_for("index"))
        else:
            flash("Väärä sähköpostiosoite tai salasana", "error")
            return redirect(url_for("login"))
    return render_template('login.html', form=form)

@app.route("/logout")
def logout():
    users.logout()
    return redirect(url_for("index"))

@app.route("/register", methods=["get","post"])
def register():
    form = RegisterForm(meta={'locales': ['fi_FI', 'fi']})
    if form.validate_on_submit():
        email = request.form["email"]
        password = request.form["password"]
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        nickname = request.form["nickname"]
        gender = int(request.form["gender"])
        birth_date = datetime.datetime.strptime(request.form["birth_date"], '%d.%m.%Y')
        profile = request.form["profile"]    
        if users.register(email,password, first_name, last_name, nickname, gender, birth_date, profile):
            flash("Käyttäjätunnus luotu", "success")
            return redirect(url_for("index"))
        else:
            flash("Rekisteröinti ei onnistunut", "error")
            return redirect(url_for("register"))
    return render_template("register.html", form=form)