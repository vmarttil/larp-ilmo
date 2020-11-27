import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, IntegerField, TextAreaField, DateField, HiddenField
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
    gender = RadioField('Sukupuoli', widget=ListWidget(), choices=[
        ('0', 'En halua kertoa'),
        ('1', 'Mies'),
        ('3', 'Nainen'),
        ('9', 'Muu')])
    birth_year = StringField('Syntymävuosi', widget=TextInput(), validators=[
        Regexp('(19[0-9]{1})|(20[0-2][0-9])', message='Anna kelvollinen syntymävuosi')])
    profile = TextAreaField('Pelaajaprofiilikuvaus', widget=TextArea(), validators=[
        Length(min=10, max=1000, message="Profiilikuvauksen on oltava 10-1000 merkkiä pitkä")])
    submit = SubmitField('Rekisteröidy', widget=SubmitInput())

class LoginForm(FlaskForm):
    email = StringField('Sähköpostiosoite', widget=EmailInput(), validators=[
        DataRequired(message="Sähköpostiosoite on pakollinen")])
    password = PasswordField('Salasana', widget=PasswordInput(), validators=[
        DataRequired(message="Salasana on pakollinen")])
    submit = SubmitField('Kirjaudu', widget=SubmitInput())

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
    submit = SubmitField('Tallenna peli', widget=SubmitInput())

class RegistrationForm(FlaskForm):
    form_id = HiddenField()
    form_name = HiddenField()
    published = HiddenField()
    publish = SubmitField('Avaa ilmoittautuminen', widget=SubmitInput())
    cancel = SubmitField('Sulje ilmoittautuminen', widget=SubmitInput())
    submit = SubmitField('Ilmoittaudu', widget=SubmitInput())




    # string_fields = FieldList(FormField(StringFieldForm), min_entries=0)
    # integer_fields = FieldList(FormField(IntegerFieldForm), min_entries=0)
    # radio_fields = FieldList(FormField(RadioFieldForm), min_entries=0)
    # select_fields = FieldList(FormField(SelectFieldForm), min_entries=0)
    # select_multiple_fields = FieldList(FormField(SelectMultipleFieldForm), min_entries=0)
    # text_area_fields = FieldList(FormField(TextAreaFieldForm), min_entries=0)
    # checkbox_list_fields = FieldList(FormField(CheckboxListFieldForm), min_entries=0)

""" 
class StringFieldForm(FlaskForm):
    id = HiddenField(validators=[
        Regexp("[0-9+]" message="ID:n on oltava numero")])
    position = HiddenField(validators=[
        Regexp("[0-9+]" message="Järjestysnumeron on oltava numero")])
    field = StringField(widget=TextInput(), validators=[
        DataRequired(message="Tämä kenttä on pakollinen")])

class IntegerFieldForm(FlaskForm):
    id = HiddenField(validators=[
        Regexp("[0-9+]" message="ID:n on oltava numero")])
    position = HiddenField(validators=[
        Regexp("[0-9+]" message="Järjestysnumeron on oltava numero")])
    field = IntegerField(widget=numberInput(), validators=[
        DataRequired(message="Tämä kenttä on pakollinen"),
        Regexp("[0-9+]" message="Arvon on oltava lukuarvo")])

class RadioFieldForm(FlaskForm):
    id = HiddenField(validators=[
        Regexp("[0-9+]" message="ID:n on oltava numero")])
    position = HiddenField(validators=[
        Regexp("[0-9+]" message="Järjestysnumeron on oltava numero")])
    field = RadioField(widget=ListInput(), validators=[
        DataRequired(message="Tämä valinta on pakollinen")])

class SelectFieldForm(FlaskForm):
    id = HiddenField(validators=[
        Regexp("[0-9+]" message="ID:n on oltava numero")])
    position = HiddenField(validators=[
        Regexp("[0-9+]" message="Järjestysnumeron on oltava numero")])
    field = SelectField(widget=Select(multiple=False), validators=[
        DataRequired(message="Tämä valinta on pakollinen")])
    def iter_choices(self):
        for value, label, selected in self.choices:
            yield (value, label, selected)

class SelectMultipleFieldForm(FlaskForm):
    id = HiddenField(validators=[
        Regexp("[0-9+]" message="ID:n on oltava numero")])
    position = HiddenField(validators=[
        Regexp("[0-9+]" message="Järjestysnumeron on oltava numero")])
    field = SelectMultipleField(widget=Select(multiple=True), validators=[
        DataRequired(message="valitse vähintään yksi vaihtoehto")])
    def iter_choices(self):
        for value, label, selected in self.choices:
            yield (value, label, selected)

class TextAreaFieldForm(FlaskForm):
    id = HiddenField(validators=[
        Regexp("[0-9+]" message="ID:n on oltava numero")])
    position = HiddenField(validators=[
        Regexp("[0-9+]" message="Järjestysnumeron on oltava numero")])
    field = StringField(widget=TextArea())

class CheckboxFieldForm(FlaskForm):
    id = HiddenField(validators=[
        Regexp("[0-9+]" message="ID:n on oltava numero")])
    position = HiddenField(validators=[
        Regexp("[0-9+]" message="Järjestysnumeron on oltava numero")])
    field = FieldList(CheckboxField(), min_entries=1) """