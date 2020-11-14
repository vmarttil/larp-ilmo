from flask import Flask
from os import getenv

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

import routes


@app.template_filter('formatdate')
def format_date(date, format="%-d.%-m.%Y"):
    if date is None:
        return ""
    return date.strftime(format)

@app.context_processor
def format_daterange():
    def _format_daterange(start_date, end_date):
        format="%-d.%-m.%Y"
        month_format="%-d.%-m."
        day_format="%-d."
        if start_date.year == end_date.year:
            if start_date.month == end_date.month:
                return start_date.strftime(day_format) + "–" + end_date.strftime(format)
            else:
                return start_date.strftime(month_format) + "–" + end_date.strftime(format)
        else: 
            return start_date.strftime(format) + "–" + end_date.strftime(format)
    return dict(format_daterange=_format_daterange)

@app.context_processor
def format_name():
    def _format_name(first_name, last_name, nickname):
        if nickname == "":
            return first_name + ' ' + last_name
        else: 
            return first_name + ' "' + nickname + '" ' + last_name
    return dict(format_name=_format_name)