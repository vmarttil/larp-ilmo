from flask import Flask
from os import getenv
from flask_bootstrap import Bootstrap
from flask_datepicker import datepicker

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
bootstrap = Bootstrap(app)
datepicker(app=app, local=['static/js/jquery-ui.js', 'static/styles/jquery-ui.css'])

import routes.main
import routes.game
import routes.form