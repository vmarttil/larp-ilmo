from db import db
import users

def get_list():
    sql = "SELECT id, name, start_date, end_date, location FROM Game ORDER BY start_date"
    result = db.session.execute(sql)
    return result.fetchall()

def get_details(id):
    sql = "SELECT * FROM Game WHERE id = :id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()

def send(name, start_date, end_date, location, description):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO Game (name, start_date, end_date, location, description) VALUES (:name, :start_date, :end_date, :location, :description)"
    db.session.execute(sql, {"name":name, "start_date":start_date, "end_date":end_date, "location":location, "description":description})
    sql = "SELECT CURRVAL(pg_get_serial_sequence('Game','id'))"
    result = db.session.execute(sql)
    game_id = result.fetchone()[0]
    sql = "INSERT INTO GameOrganiser (user_id, game_id) VALUES (:user_id, :game_id)"
    db.session.execute(sql, {"user_id":user_id, "game_id":game_id})
    db.session.commit()
    return True