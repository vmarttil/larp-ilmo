import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, IntegerField, TextAreaField, DateField, HiddenField
from wtforms.validators import DataRequired, Email, Length, NumberRange

class RegisterForm(FlaskForm):
    email = StringField('Sähköpostiosoite: ', validators=[
        DataRequired(message="Sähköpostiosoite on pakollinen"),
        Email(message="Anna kelvollinen sähköpostiosoite")])
    password = PasswordField('Salasana: ', validators=[
        DataRequired(message="Salasana on pakollinen"),
        Length(min=6, max=24, message="Salasanan on oltava 6-24 merkkiä pitkä")])
    first_name = StringField('Etunimi: ', validators=[
        DataRequired(message="Etunimi on pakollinen")])
    last_name = StringField('Sukunimi: ', validators=[
        DataRequired(message="Sukunimi on pakollinen")])
    nickname = StringField('Lempinimi: ')        
    gender = RadioField('Sukupuoli: ', choices=[
        ('0', 'En halua kertoa'),
        ('1', 'Mies'),
        ('3', 'Nainen'),
        ('9', 'Muu')])
    birth_year = IntegerField('Syntymävuosi: ', validators=[
        NumberRange(min=int(datetime.datetime.now().year) - 99, max=int(datetime.datetime.now().year), message="Anna kelvollinen syntymävuosi")])
    profile = TextAreaField('Pelaajaprofiilikuvaus: ', validators=[
        Length(min=10, max=1000, message="Profiilikuvauksen on oltava 10-1000 merkkiä pitkä")])
    submit = SubmitField('Rekisteröidy')

class LoginForm(FlaskForm):
    email = StringField('Sähköpostiosoite: ', validators=[
        DataRequired(message="Sähköpostiosoite on pakollinen")])
    password = PasswordField('Salasana: ', validators=[
        DataRequired(message="Salasana on pakollinen")])
    submit = SubmitField('Kirjaudu')

class GameForm(FlaskForm):
    id = HiddenField()
    name = StringField('Pelin nimi: ', validators=[
        DataRequired(message="Nimi on pakollinen")])
    start_date = DateField('Pelin alkupäivämäärä: ')
    end_date = DateField('Pelin loppupäivämäärä: ')
    location = StringField('Pelin sijainti: ')
    price = IntegerField('Pelin hinta: ')
    description = TextAreaField('Pelin kuvaus: ', validators=[
        DataRequired(message="Kuvaus on pakollinen"),
        Length(min=10, max=1000, message="Kuvauksen on oltava 10-1000 merkkiä pitkä")])
    submit = SubmitField('Tallenna peli')


