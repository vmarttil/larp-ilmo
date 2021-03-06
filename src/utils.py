from app import app

def to_dict_list(result):
    '''Convert a list of named tuples from an SQL query to a list of dictionaries.'''
    itemlist = []
    for item in result:
        itemlist.append(dict(item))
    return itemlist

@app.template_filter('formatdate')
def format_date(date, format="%-d.%-m.%Y"):
    '''Format a date to the Finnish format ('dd.mm.yyyy') and return as string.'''
    if date is None:
        return ""
    return date.strftime(format)

@app.template_filter('formattimestamp')
def format_timestamp(timestamp, format="%-d.%-m.%Y klo %H.%M.%S"):
    '''Format a timestamp to the Finnish format ('dd.mm.yyyy klo hh.mm.ss') and return as string.'''
    if timestamp is None:
        return ""
    return timestamp.strftime(format)

@app.context_processor
def format_daterange():
    def _format_daterange(start_date, end_date):
        '''Format a date range to the Finnish format, taking into account shared components, and return as string.'''
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
        '''Format a name, consisting of a first name, last name and nickname into a single string.'''
        if nickname == "":
            return first_name + ' ' + last_name
        else: 
            return first_name + ' "' + nickname + '" ' + last_name
    return dict(format_name=_format_name)