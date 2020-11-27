import sys
from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

def login(email,password):
    sql = "SELECT password, id, first_name, last_name, nickname FROM Person WHERE email=:email"
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

def register(email,password, first_name, last_name, nickname, gender, birth_year, profile):
    hash_value = generate_password_hash(password)
    print("Email: " + email + " Password: " + password + " First name: " + first_name + " Last name: " + last_name + " Nickname: " + nickname + " Gender: " + str(gender) + " Birth year: " + str(birth_year) + " Profile: " + profile)
    try:
        sql = "INSERT INTO Person (email, password, first_name, last_name, nickname, gender, birth_year, profile) VALUES (:email, :password, :first_name, :last_name, :nickname, :gender, :birth_year, :profile)"
        db.session.execute(sql, {"email":email, "password":hash_value, "first_name":first_name, "last_name":last_name, "nickname":nickname, "gender":gender, "birth_year":birth_year, "profile":profile})
        db.session.commit()
    except:
        return False
    print("Käyttäjätunnuksen tallennus onnistui.")
    return login(email,password)

def user_id():
    return session.get("user_id",0)

def user_name():
    return session.get("user_name","")

def format_name(first_name, last_name, nickname):
    if nickname == "":
        return first_name + ' ' + last_name
    else: 
        return first_name + ' "' + nickname + '" ' + last_name