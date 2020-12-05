import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, IntegerField, TextAreaField, DateField, HiddenField, SelectField
from wtforms.widgets import TextInput, TextArea, PasswordInput, CheckboxInput, SubmitInput, ListWidget, Select
from wtforms.widgets.html5 import DateInput, DateTimeInput, EmailInput, NumberInput
from wtforms.validators import DataRequired, Email, Length, NumberRange, Regexp, ValidationError

class RegisterForm(FlaskForm):
    email = StringField('Sähköpostiosoite', widget=EmailInput(), validators=[
        DataRequired(message="Sähköpostiosoite on pakollinen"),
        Email(message="Anna kelvollinen sähköpostiosoite")])
    password = PasswordField('Salasana', widget=PasswordInput(), validators=[
        DataRequired(message="Salasana on pakollinen"),
        Length(min=6, max=24, message="Salasanan on oltava 6-24 merkkiä pitkä")])
    first_name = StringField('Etunimi', widget=TextInput(), validators=[
        DataRequired(message="Etunimi on pakollinen")])
    last_name = StringField('Sukunimi', widget=TextInput(), validators=[
        DataRequired(message="Sukunimi on pakollinen")])
    nickname = StringField('Lempinimi', widget=TextInput())
    phone = StringField('Puhelinnumero', widget=TextInput(), validators=[
        Regexp('^\+\d+$', message='Anna kelvollinen puhelinnumero muodossa +xxxxxxxxxxxxx')])
    birth_date = StringField('Syntymäaika', widget=TextInput(), validators=[
        Regexp('^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[012])\.(19|20)\d\d$', message='Anna kelvollinen päivämäärä')])
    profile = TextAreaField('Pelaajaprofiilikuvaus', widget=TextArea(), validators=[
        Length(min=10, max=1000, message="Profiilikuvauksen on oltava 10-1000 merkkiä pitkä")])
    submit = SubmitField('Rekisteröidy', widget=SubmitInput())

class LoginForm(FlaskForm):
    email = StringField('Sähköpostiosoite', widget=EmailInput(), validators=[
        DataRequired(message="Sähköpostiosoite on pakollinen")])
    password = PasswordField('Salasana', widget=PasswordInput(), validators=[
        DataRequired(message="Salasana on pakollinen")])
    submit = SubmitField('Kirjaudu', widget=SubmitInput())

class ProfileForm(FlaskForm):
    first_name = StringField('Etunimi', widget=TextInput(), validators=[
        DataRequired(message="Etunimi on pakollinen")])
    last_name = StringField('Sukunimi', widget=TextInput(), validators=[
        DataRequired(message="Sukunimi on pakollinen")])
    nickname = StringField('Lempinimi', widget=TextInput())        
    phone = StringField('Puhelinnumero', widget=TextInput(), validators=[
        Regexp('^\+\d+$', message='Anna kelvollinen puhelinnumero muodossa +xxxxxxxxxxxxx')])
    birth_date = StringField('Syntymäaika', widget=TextInput(), validators=[
        Regexp('^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[012])\.(19|20)\d\d$', message='Anna kelvollinen päivämäärä')])
    profile = TextAreaField('Pelaajaprofiilikuvaus', widget=TextArea(), validators=[
        Length(min=10, max=1000, message="Profiilikuvauksen on oltava 10-1000 merkkiä pitkä")])
    submit = SubmitField('Tallenna muutokset', widget=SubmitInput())

class GameForm(FlaskForm):
    id = HiddenField()
    name = StringField('Pelin nimi', widget=TextInput(), validators=[
        DataRequired(message="Nimi on pakollinen")])
    start_date = StringField('Pelin alkupäivämäärä', widget=TextInput(), validators=[
        Regexp('^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[012])\.(20)\d\d$', message='Anna kelvollinen päivämäärä')])
    end_date = StringField('Pelin loppupäivämäärä', widget=TextInput(), validators=[
        Regexp('^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[012])\.(20)\d\d$', message='Anna kelvollinen päivämäärä')])
    location = StringField('Pelin sijainti', widget=TextInput())
    price = IntegerField('Pelin hinta', widget=NumberInput(), validators=[
        NumberRange(min=0, max=9999, message='Hinnan on oltava 0-9999')])
    description = TextAreaField('Pelin kuvaus', widget=TextArea(), validators=[
        DataRequired(message="Kuvaus on pakollinen"),
        Length(min=10, max=1000, message="Kuvauksen on oltava 10-1000 merkkiä pitkä")])
    create_form = SubmitField('Luo ilmoittautumislomake', widget=SubmitInput())
    edit_form = SubmitField('Muokkaa ilmoittautumislomaketta', widget=SubmitInput())
    publish_form = SubmitField('Avaa ilmoittautuminen', widget=SubmitInput())
    unpublish_form = SubmitField('Sulje ilmoittautuminen', widget=SubmitInput())
    submit = SubmitField('Tallenna pelin tiedot', widget=SubmitInput())

class RegistrationForm(FlaskForm):
    form_id = HiddenField()
    form_name = HiddenField()
    published = HiddenField()
    publish = SubmitField('Avaa ilmoittautuminen', widget=SubmitInput())
    cancel = SubmitField('Sulje ilmoittautuminen', widget=SubmitInput())
    submit = SubmitField('Ilmoittaudu', widget=SubmitInput())

class FormEditForm(FlaskForm):
    form_id = HiddenField()
    form_name = HiddenField()
    add_question = SubmitField('Lisää', widget=SubmitInput())

class NewQuestionForm(FlaskForm):
    form_id = HiddenField()
    field_type = HiddenField()
    text = StringField('Kysymysteksti', widget=TextInput(), validators=[
        DataRequired(message="Kysymysteksti on pakollinen")])
    description = TextAreaField('Selitysteksti', widget=TextArea(), validators=[
        Length(min=0, max=200, message="Selitystekstin on oltava 0-200 merkkiä pitkä")])
    submit = SubmitField('Tallenna kysymys', widget=SubmitInput())