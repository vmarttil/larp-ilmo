from db import db
import users

def get_list():
    sql =  "SELECT \
                g.id, \
                g.name, \
                g.start_date, \
                g.end_date, \
                g.location, \
                g.price, \
                go.person_id AS organiser_id, \
                f.published, \
                COUNT(r.person_id) AS num_registrations \
            FROM Game AS g \
                JOIN GameOrganiser AS go \
                    ON g.id = go.game_id \
                LEFT JOIN Form AS f \
                    ON g.id = f.game_id \
                LEFT JOIN Registration as r \
                    ON g.id = r.game_id \
            GROUP BY g.id, g.name, g.start_date, g.end_date, g.location, g.price, go.person_id, f.published \
            ORDER BY start_date"
    result = db.session.execute(sql)
    game_list = result.fetchall()
    return game_list

def get_details(id):
    sql_game = "SELECT \
                    g.id, \
                    g.name, \
                    g.start_date, \
                    g.end_date, \
                    g.location, \
                    g.price, \
                    g.description, \
                    f.published \
                    FROM Game AS g\
                        LEFT JOIN Form AS f \
                            ON g.id = f.game_id \
                    WHERE g.id = :id"
    result_game = db.session.execute(sql_game, {"id":id})
    game = result_game.fetchone()
    organisers = get_organisers(id)
    game = dict(game.items())
    game['organisers'] = organisers
    return game

def get_organisers(game_id):
    sql_orgs =  "SELECT \
                    p.id, \
                    p.first_name, \
                    p.last_name, \
                    p.nickname, \
                    p.email \
                FROM Person AS p \
                    JOIN GameOrganiser AS go \
                        ON p.id = go.person_id \
                WHERE go.game_id = :id \
                ORDER BY p.last_name"
    result_orgs = db.session.execute(sql_orgs, {"id":game_id})
    organisers = result_orgs.fetchall()
    return organisers

def get_registrations(game_id):
    sql_regs =  "SELECT \
                    ROW_NUMBER() OVER (ORDER BY r.submitted ASC) AS number, \
                    r.id, \
                    p.first_name, \
                    p.last_name, \
                    p.nickname, \
                    r.submitted \
                FROM Registration AS r \
                    JOIN Person AS p \
                        ON r.person_id = p.id \
                WHERE r.game_id = :id \
                ORDER BY r.submitted ASC"
    result_regs = db.session.execute(sql_regs, {"id":game_id})
    registrations = result_regs.fetchall()
    return registrations

def get_registration_game(registration_id):
    sql =  "SELECT \
                game_id \
            FROM Registration \
            WHERE id = :registration_id"
    result = db.session.execute(sql, {"registration_id": registration_id})
    game_id = result.fetchone()[0]
    return game_id

def send(id, name, start_date, end_date, location, price, description):
    person_id = users.user_id()
    if person_id == 0:
        return False
    if id is None:
        sql =  "INSERT INTO Game (\
                    name, \
                    start_date, \
                    end_date, \
                    location, \
                    price, \
                    description \
                ) \
                VALUES ( \
                    :name, \
                    :start_date, \
                    :end_date, \
                    :location, \
                    :price, \
                    :description \
                )"
        db.session.execute(sql, {"name":name, "start_date":start_date, "end_date":end_date, "location":location, "price":price, "description":description})
        sql = "SELECT CURRVAL(pg_get_serial_sequence('Game','id'))"
        result = db.session.execute(sql)
        game_id = result.fetchone()[0]
        sql =  "INSERT INTO GameOrganiser ( \
                    person_id, \
                    game_id \
                ) \
                VALUES ( \
                    :person_id, \
                    :game_id \
                );"
        db.session.execute(sql, {"person_id":person_id, "game_id":game_id})
    else: 
        sql =  "UPDATE Game SET \
                    name=:name, \
                    start_date=:start_date, \
                    end_date=:end_date, \
                    location=:location, \
                    price=:price, \
                    description=:description \
                WHERE id=:id"
        db.session.execute(sql, {"name":name, "start_date":start_date, "end_date":end_date, "location":location, "price":price, "description":description, "id":id})
    db.session.commit()
    return True
