import sys
from app import app
from flask import render_template, request, redirect, flash, url_for
import games, users, gameforms, questions
from forms import *

@app.route("/game/<game_id>/form/edit", methods=["get", "post"])
def editform(game_id):
    '''Display the registration form editor on GET and open the new question editor on POST.'''
    game = games.get_details(game_id)
    if users.user_id() not in map(lambda org: org['id'], game['organisers']):
        return redirect(url_for("index"))
    gameform = gameforms.get_game_form(game_id)
    form_data = {"form_id": gameform['id'], "form_name": gameform['name']}
    form = FormEditForm(data=form_data, meta={'locales': ['fi_FI', 'fi']})
    field_types = gameforms.get_field_types()
    if request.method == 'GET':
        question_list = gameforms.get_form_questions(gameform['id'])        
        for question in question_list:
            question['options'] = questions.get_question_options(int(question['id']))
        return render_template("form_editor.html", game=game, form=form, question_list=question_list, field_types=field_types, action="/game/" + game_id + "/form/edit", title="Ilmoittautumislomakkeen muokkaus")    
    elif form.validate_on_submit() and request.form.get('field_type'):
        form_data = {"form_id": request.form['form_id'], "field_type": request.form['field_type'], "text": "", "description": ""}
        field_type_name = gameforms.get_field_type_name(request.form['field_type'])
        form = NewQuestionForm(data=form_data, meta={'locales': ['fi_FI', 'fi']})
        return render_template("new_question.html", form=form, game=game, options=[], action="/game/" + game_id + "/form/edit/new_question", title="Uuden kysymyksen luonti: " + field_type_name)
    else:
        return redirect("/game/" + game_id + "/form/edit")

@app.route("/game/<game_id>/form/preview", methods=["get"])
def previewform(game_id):
    '''Display an inactive preview of the current registration form.'''
    game = games.get_details(game_id)
    if users.user_id() not in map(lambda org: org['id'], game['organisers']):
        return redirect(url_for("index"))
    gameform = gameforms.get_game_form(game_id)
    form_data = {"form_id": gameform['id'], "form_name": gameform['name']}
    form = RegistrationForm(data=form_data, meta={'locales': ['fi_FI', 'fi']})
    question_list = gameforms.get_form_questions(gameform['id'])        
    for question in question_list:
        question['options'] = questions.get_question_options(int(question['id']))
    return render_template("form_preview.html", game=game, form=form, question_list=question_list, action="", title="Ilmoittautumislomakkeen esikatselu")

@app.route("/game/<game_id>/form/edit/move_up", methods=["post"])
def editform_move_up(game_id):
    '''Move the submitting question upward one step and return to the form editor.'''
    form_id = request.form["form_id"]
    current_pos = request.form["move_up"]
    questions.move_question_up(form_id, current_pos)
    return redirect("/game/" + game_id + "/form/edit")

@app.route("/game/<game_id>/form/edit/move_down", methods=["post"])
def editform_move_down(game_id):
    '''Move the submitting question downward one step and return to the form editor.'''
    form_id = request.form["form_id"]
    current_pos = request.form["move_down"]
    questions.move_question_down(form_id, current_pos)
    return redirect("/game/" + game_id + "/form/edit")

@app.route("/game/<game_id>/form/edit/edit_question", methods=["post"])
def editform_edit_question(game_id):
    '''Display the editing page for the submitting question.'''
    if request.form.get('add_option') or request.form.get('delete_option'):
        game = games.get_details(game_id)
        options = []
        for field, value in request.form.items():
            if 'option_text' in field and value.strip() != '' and request.form.get('delete_option') != value:
                options.append(value.strip())
        form_data = request.form
        form = EditQuestionForm(data=form_data, meta={'locales': ['fi_FI', 'fi']})
        field_type_name = gameforms.get_field_type_name(request.form['field_type'])
        return render_template("edit_question.html", form=form, game=game, options=options, action="/game/" + game_id + "/form/edit/update_question", title="Kysymyksen muokkaus: " + field_type_name)
    else: 
        game = games.get_details(game_id)
        question = questions.get_question(request.form["edit_question"])
        form_data = {"formquestion_id": question['id'], "field_type": str(question['field_type']), "text": question['text'], "description": question['description']}
        form = EditQuestionForm(data=form_data, meta={'locales': ['fi_FI', 'fi']})
        field_type_name = gameforms.get_field_type_name(question['field_type'])    
        options = map(lambda d: d['text'], question['options'])
        return render_template("edit_question.html", form=form, game=game, options=options, action="/game/" + game_id + "/form/edit/update_question", title="Kysymyksen muokkaus: " + field_type_name)
    
@app.route("/game/<game_id>/form/edit/update_question", methods=["post"])
def editform_update_question(game_id):
    '''Save the properties of the question contained in the submitted form.'''
    question_text = request.form["text"]
    description = request.form["description"]
    options = []
    for field, value in request.form.items():
        if 'option_text' in field and value.strip() != '':
            options.append(value.strip())
    if questions.update_question(request.form["formquestion_id"], question_text, description, options):
        flash("Kysymystä muokattu", "success")
        return redirect("/game/" + game_id + "/form/edit")
    else:
        flash("Kysymyksen muokkaaminen ei onnistunut", "error")
        return redirect("/game/" + game_id + "/form/edit")

@app.route("/game/<game_id>/form/edit/delete_question", methods=["post"])
def editform_delete(game_id):
    '''Delete the submitting question.'''
    if request.form.get('delete_question'):
        formquestion_id = request.form['delete_question']
        form_data = {"attribute": formquestion_id}
        form = PopupForm(data=form_data, meta={'locales': ['fi_FI', 'fi']})
        paragraphs = ["Oletko varma, että haluat poistaa kysymyksen:", "'" + questions.get_question_text(formquestion_id) + "'"]
        return render_template("popup.html", form=form, action="/game/" + game_id + "/form/edit/delete_question", title="Poista kysymys", paragraphs=paragraphs)
    if request.form.get('submit'):
        if questions.delete_question(request.form['attribute']):
            flash("Kysymys poistettu", "success")
            return redirect("/game/" + game_id + "/form/edit")
        else:
            flash("Kysymyksen poistaminen ei onnistunut", "error")
            return redirect("/game/" + game_id + "/form/edit")
    else: 
        return redirect("/game/" + game_id + "/form/edit")

@app.route("/game/<game_id>/form/edit/new_question", methods=["post"])
def editform_new_question(game_id):
    '''Save the contents of the submitted form as a new question in the database.'''
    form_id = request.form["form_id"]
    field_type = request.form["field_type"]
    question_text = request.form["text"]
    description = request.form["description"]
    options = []
    for field, value in request.form.items():
        if 'option_text' in field and value.strip() != '':
            options.append(value.strip())
    position = gameforms.get_last_position(form_id)
    if questions.add_new_question(form_id, field_type, question_text, description, options, position):
        flash("Kysymys lisätty", "success")
        return redirect("/game/" + game_id + "/form/edit")
    else:
        flash("Kysymyksen lisääminen ei onnistunut", "error")
        return redirect("/game/" + game_id + "/form/edit")

@app.route("/game/<game_id>/form/edit/new_question/new_option", methods=["post"])
def editform_new_question_new_option(game_id):
    '''Add a new option to the list of options contained in the form and display the updated question edit view.'''
    game = games.get_details(game_id)
    options = []
    for field, value in request.form.items():
        if 'option_text' in field and value.strip() != '':
            options.append(value.strip())
    form_data = request.form
    form = NewQuestionForm(data=form_data, meta={'locales': ['fi_FI', 'fi']})
    field_type_name = gameforms.get_field_type_name(request.form['field_type'])
    return render_template("new_question.html", form=form, game=game, options=options, action="/game/" + game_id + "/form/edit/new_question", title="Uuden kysymyksen luonti: " + field_type_name)