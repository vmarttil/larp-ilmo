import sys
from datetime import datetime
from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

def login(email,password):
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
    del session['user_id']
    del session['user_name']

def register(email,password, first_name, last_name, nickname, gender, birth_date, profile):
    hash_value = generate_password_hash(password)
    try:
        sql =  "INSERT INTO Person (\
                    email, \
                    password, \
                    first_name, \
                    last_name, \
                    nickname, \
                    gender, \
                    birth_date, \
                    profile\
                    ) VALUES ( \
                        :email, \
                        :password, \
                        :first_name, \
                        :last_name, \
                        :nickname, \
                        :gender, \
                        :birth_date, \
                        :profile \
                    )"
        db.session.execute(sql, {"email":email, "password":hash_value, "first_name":first_name, "last_name":last_name, "nickname":nickname, "gender":gender, "birth_date":birth_date, "profile":profile})
        db.session.commit()
    except:
        return False
    return login(email,password)

def update(first_name, last_name, nickname, gender, birth_date, profile):
    try:
        sql =  "UPDATE Person \
                    SET \
                        first_name = :first_name, \
                        last_name = :last_name, \
                        nickname = :nickname, \
                        gender = :gender, \
                        birth_date = :birth_date, \
                        profile = profile \
                    WHERE id = :id"
        db.session.execute(sql, {"id":user_id(), "first_name":first_name, "last_name":last_name, "nickname":nickname, "gender":gender, "birth_date":birth_date, "profile":profile})
        db.session.commit()
    except:
        return False
    return True

def user_id():
    return session.get("user_id",0)

def user_name():
    return session.get("user_name","")

def get_profile():
    user_id = session.get("user_id",0)
    sql =  "SELECT \
                id, \
                email, \
                first_name, \
                last_name, \
                nickname, \
                gender, \
                birth_date, \
                profile \
            FROM Person \
            WHERE id = :user_id;"
    result = db.session.execute(sql, {"user_id": user_id})
    user_profile = dict(result.fetchone())
    return user_profile

def get_registrations():
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
    registrations = result_regs.fetchall()
    return registrations

def get_prefill_data(game):
    user_id = session.get("user_id",0)
    sql =  "SELECT \
                email, \
                first_name, \
                last_name, \
                nickname, \
                birth_date, \
                profile \
            FROM Person \
            WHERE id = :user_id;"
    result = db.session.execute(sql, {"user_id": user_id})
    profile = result.fetchone()
    prefill_data = {"name": format_name(profile[1], profile[2], profile[3]), "email": profile[0], "age": calculate_age(profile[4], game["start_date"]), "profile": profile[5]}
    return prefill_data

def format_name(first_name, last_name, nickname):
    if nickname == "":
        return first_name + ' ' + last_name
    else: 
        return first_name + ' "' + nickname + '" ' + last_name

def calculate_age(birth_date, target_date):
    age = target_date.year - birth_date.year
    if target_date.month < birth_date.month or (target_date.month == birth_date.month and target_date.day < birth_date.day):
        age -= 1
    return age