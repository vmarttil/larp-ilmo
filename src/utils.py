def to_dict_list(result):
    itemlist = []
    for item in result:
        itemlist.append(dict(item))
    return itemlist