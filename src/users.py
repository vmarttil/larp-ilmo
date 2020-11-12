import sys
from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

def login(email,password):
    print("Sisäänkirjausskripti käynnistyi", file=sys.stdout)
    sql = "SELECT password, id, name FROM Person WHERE email=:email"
    result = db.session.execute(sql, {"email":email})
    user = result.fetchone()
    if user == None:
        return False
    else:
        if check_password_hash(user[0],password):
            session["user_id"] = user[1]
            session["user_name"] = user[2]
            return True
        else:
            return False

def logout():
    del session["user_id"]
    del session["user_name"]

def register(email,password, name, gender, birth_year, profile):
    print("Rekisteröintiskripti käynnistyy", file=sys.stdout)
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO Person (email, password, name, gender, birth_year, profile) VALUES (:email, :password, :name, :gender, :birth_year, :profile)"
        db.session.execute(sql, {"email":email, "password":hash_value, "name":name, "gender":gender, "birth_year":birth_year, "profile":profile})
        db.session.commit()
    except:
        print("Rekisteröinti epäonnistui")
        return False
    return login(email,password)

def user_id():
    return session.get("user_id",0)

def user_name():
    return session.get("user_name","")