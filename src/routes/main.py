import sys
from app import app
from flask import render_template, request, redirect, flash, url_for, session
import datetime
import games, users, gameforms, questions, answers
from forms import *

@app.route("/")
def index():
    '''Display the main index page.'''
    game_list = games.get_list()
    return render_template("index.html", games=game_list)


@app.route("/user/profile", methods=["get", "post"])
def editprofile():
    '''Display the profile page of the current user on GET and update it on POST.'''
    if users.user_id() == 0:
        return redirect(url_for("index"))
    profile = users.get_profile()
    profile['birth_date'] = profile['birth_date'].strftime('%d.%m.%Y')
    form = ProfileForm(data=profile, meta={'locales': ['fi_FI', 'fi']})
    if form.validate_on_submit():
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        nickname = request.form["nickname"]
        phone = request.form["phone"]
        birth_date = datetime.datetime.strptime(request.form["birth_date"], '%d.%m.%Y')
        profile = request.form["profile"]    
        if users.update(first_name, last_name, nickname, phone, birth_date, profile):
            flash("Käyttäjäprofiili päivitetty", "success")
            return redirect(url_for("editprofile"))
        else:
            flash("Käyttäjäprofiilin päivitys ei onnistunut", "error")
            return redirect(url_for("editprofile"))
    registrations = users.get_registrations()
    return render_template("profile.html", form=form, email=profile['email'], registrations=registrations, title=session.get("user_name","") + ": Käyttäjäprofiili")

@app.route("/user/profile/registration/<registration_id>", methods=["get"])
def viewpersonregistration(registration_id):
    '''Display the selected registration of the current user.'''
    if users.user_id() != games.get_registration_person(registration_id):
        return redirect(url_for("index"))
    user_profile = users.get_profile()
    game_id = games.get_registration_game(registration_id)
    game = games.get_details(game_id)
    gameform = gameforms.get_game_form(game_id)
    form_data = {"form_id": gameform['id'], "form_name": gameform['name'], "published": gameform['published']}
    form = RegistrationForm(data=form_data, meta={'locales': ['fi_FI', 'fi']})
    question_list = gameforms.get_form_questions(gameform['id'])        
    for question in question_list:
        question['options'] = questions.get_question_options(question['id'])
        question['answer'] = answers.get_question_answer(registration_id, question['id'])
    return render_template("registration.html", form=form, question_list=question_list, action="", title="Ilmoittautuminen: " + game['name'], mode="person")

@app.route("/login", methods=["get","post"])
def login():
    '''Display the login page on GET and log in the user on POST.'''
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
    '''Log out the user and display the main index page.'''
    users.logout()
    return redirect(url_for("index"))

@app.route("/register", methods=["get","post"])
def register():
    '''Display the user registration page on GET and register and log in the new user on POST.'''
    form = RegisterForm(meta={'locales': ['fi_FI', 'fi']})
    if form.validate_on_submit():
        email = request.form["email"]
        password = request.form["password"]
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        nickname = request.form["nickname"]
        phone = request.form["phone"]
        birth_date = datetime.datetime.strptime(request.form["birth_date"], '%d.%m.%Y')
        profile = request.form["profile"]    
        if users.register(email,password, first_name, last_name, nickname, phone, birth_date, profile):
            flash("Käyttäjätunnus luotu", "success")
            return redirect(url_for("index"))
        else:
            flash("Rekisteröinti ei onnistunut", "error")
            return redirect(url_for("register"))
    return render_template("register.html", form=form)