def to_dict_list(result):
    '''Convert a list of named tuples from an SQL query to a list of dictionaries.'''
    itemlist = []
    for item in result:
        itemlist.append(dict(item))
    return itemlist