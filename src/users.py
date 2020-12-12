import sys
import utils
from datetime import datetime
from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

def login(email,password):
    '''Check whether the given password corresponds to the email address and log the user in if it does.'''
    sql =  "SELECT \
                password, \
                id, \
                first_name, \
                last_name, \
                nickname \
            FROM Person \
            WHERE email = :email"
    result = db.session.execute(sql, {"email":email})
    user = result.fetchone()
    if user == None:
        print("Sisäänkirjaus epäonnistui.")
        return False
    else:
        if check_password_hash(user[0],password):
            session['user_id'] = user[1]
            session['user_name'] = format_name(user[2], user[3], user[4])
            return True
        else:
            print("Sisäänkirjaus epäonnistui.")
            return False

def logout():
    '''Log out the user and remove his data from the session.'''
    del session['user_id']
    del session['user_name']

def register(email,password, first_name, last_name, nickname, phone, birth_date, profile):
    '''Register a new user and enter their information into the database.'''
    hash_value = generate_password_hash(password)
    try:
        sql =  "INSERT INTO Person (\
                    email, \
                    password, \
                    first_name, \
                    last_name, \
                    nickname, \
                    phone, \
                    birth_date, \
                    profile\
                    ) VALUES ( \
                    :email, \
                    :password, \
                    :first_name, \
                    :last_name, \
                    :nickname, \
                    :phone, \
                    :birth_date, \
                    :profile \
                )"
        db.session.execute(sql, {"email":email, "password":hash_value, "first_name":first_name, "last_name":last_name, "nickname":nickname, "phone":phone, "birth_date":birth_date, "profile":profile})
        db.session.commit()
    except:
        return False
    return login(email,password)

def update(first_name, last_name, nickname, phone, birth_date, profile):
    '''Update the profile information for the currently logged in user.'''
    try:
        sql =  "UPDATE Person \
                    SET \
                        first_name = :first_name, \
                        last_name = :last_name, \
                        nickname = :nickname, \
                        phone = :phone, \
                        birth_date = :birth_date, \
                        profile = profile \
                    WHERE id = :id"
        db.session.execute(sql, {"id":user_id(), "first_name":first_name, "last_name":last_name, "nickname":nickname, "phone":phone, "birth_date":birth_date, "profile":profile})
        db.session.commit()
    except:
        return False
    return True

def user_id():
    '''Return the user of the currently logged in user.'''
    return session.get("user_id",0)

def user_name():
    '''Return the formatted name of of the currently logged in user.'''
    return session.get("user_name","")

def get_profile():
    '''Get the full profile of the currently logged in user as a dictionary.'''
    user_id = session.get("user_id",0)
    sql =  "SELECT \
                id, \
                email, \
                first_name, \
                last_name, \
                nickname, \
                phone, \
                birth_date, \
                profile \
            FROM Person \
            WHERE id = :user_id;"
    result = db.session.execute(sql, {"user_id": user_id})
    user_profile = dict(result.fetchone())
    return user_profile

def get_registrations():
    '''Get the list of registrations for the currently logged in user as a list of dictionaries.'''
    user_id = session.get("user_id",0)
    sql_regs =  "SELECT \
                    r.id, \
                    g.name, \
                    r.submitted \
                FROM Registration AS r \
                    JOIN Game AS g \
                        ON r.game_id = g.id \
                WHERE r.person_id = :id \
                ORDER BY r.submitted ASC"
    result_regs = db.session.execute(sql_regs, {"id":user_id})
    registrations = utils.to_dict_list(result_regs.fetchall())
    return registrations

def get_prefill_data(game):
    '''Get the email, name, phone, birth date and profile of the current user for pre-filling a registration form.'''
    user_id = session.get("user_id",0)
    sql =  "SELECT \
                email, \
                first_name, \
                last_name, \
                nickname, \
                phone, \
                birth_date, \
                profile \
            FROM Person \
            WHERE id = :user_id;"
    result = db.session.execute(sql, {"user_id": user_id})
    profile = result.fetchone()
    prefill_data = {"name": format_name(profile[1], profile[2], profile[3]), "email": profile[0], "phone": profile[4], "age": calculate_age(profile[5], game["start_date"]), "profile": profile[6]}
    return prefill_data

def format_name(first_name, last_name, nickname):
    '''Format a name consistin of first and last names and optionally a nickname.'''
    if nickname == "":
        return first_name + ' ' + last_name
    else: 
        return first_name + ' "' + nickname + '" ' + last_name

def calculate_age(birth_date, target_date):
    '''Calculate the age of a person at a specific moment based on their birth date.'''
    age = target_date.year - birth_date.year
    if target_date.month < birth_date.month or (target_date.month == birth_date.month and target_date.day < birth_date.day):
        age -= 1
    return age